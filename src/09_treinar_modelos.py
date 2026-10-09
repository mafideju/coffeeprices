"""Treina baselines, modelo linear e Random Forest usando SÓ o treino (o teste não é aberto aqui)."""
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import f1_score, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import config

TAMANHO_MINIMO_TREINO_CV = 30


def parar(mensagem):
    print(f"ERRO: {mensagem}")
    sys.exit(1)


def mostrar_divisoes(treino, divisoes):
    """Imprime tamanhos e classes de cada divisão da validação cruzada temporal."""
    print(f"Validação cruzada temporal: TimeSeriesSplit(n_splits={config.N_SPLITS_CV}, "
          f"test_size={config.TAMANHO_VALIDACAO_CV}, gap={config.GAP_MESES})")
    for i, (idx_treino, idx_val) in enumerate(divisoes, start=1):
        t, v = treino.iloc[idx_treino], treino.iloc[idx_val]
        print(f"  Divisão {i}: treino {len(t)} linhas ({t['mes'].min():%Y-%m} a {t['mes'].max():%Y-%m}), "
              f"alta {int(t['alvo_alta'].sum())} e queda {int((1 - t['alvo_alta']).sum())} | "
              f"validação {len(v)} linhas ({v['mes'].min():%Y-%m} a {v['mes'].max():%Y-%m}), "
              f"alta {int(v['alvo_alta'].sum())} e queda {int((1 - v['alvo_alta']).sum())}")
        if len(t) < TAMANHO_MINIMO_TREINO_CV:
            print(f"  AVISO: o treino da divisão {i} tem só {len(t)} linhas (menos de {TAMANHO_MINIMO_TREINO_CV}); "
                  "resultado instável.")
        if t["alvo_alta"].nunique() < 2:
            parar(f"o treino da divisão {i} tem uma só classe; não dá para ajustar um classificador.")


def conferir_escala(treino):
    """acum12_passado e alvo_acum_12m precisam estar ambos em % (a persistência compara os dois)."""
    ex = treino.iloc[len(treino) // 2]
    print(f"Verificação de escala (exemplo {ex['mes']:%Y-%m}): acum12_passado = {ex['acum12_passado']:.2f}, "
          f"alvo_acum_12m = {ex['alvo_acum_12m']:.2f}")
    for col in ("acum12_passado", "alvo_acum_12m"):
        print(f"  {col}: mínimo {treino[col].min():.2f}, máximo {treino[col].max():.2f}")
    razao = treino["alvo_acum_12m"].std() / treino["acum12_passado"].std()
    if not 0.1 < razao < 10:
        parar(f"escalas divergentes (razão dos desvios-padrão = {razao:.2f}): uma coluna deve estar em fração "
              "e a outra em %. A persistência da regressão ficaria errada.")
    print(f"  Mesma unidade (%), razão dos desvios-padrão = {razao:.2f}")


def nota_classificacao(y_real, y_prev):
    return f1_score(y_real, y_prev, average="macro", labels=[0, 1], zero_division=0)


def nota_regressao(y_real, y_prev):
    return float(np.sqrt(mean_squared_error(y_real, y_prev)))


def notas_baselines(treino, divisoes):
    """Nota agrupada (previsões de validação das divisões juntas) de cada baseline."""
    reais_c, reais_r = [], []
    prev = {"maioria": [], "persistencia_sinal": [], "media": [], "persistencia": []}
    for idx_treino, idx_val in divisoes:
        t, v = treino.iloc[idx_treino], treino.iloc[idx_val]
        reais_c += list(v["alvo_alta"])
        reais_r += list(v["alvo_acum_12m"])
        prev["maioria"] += [int(t["alvo_alta"].mean() >= 0.5)] * len(v)
        prev["persistencia_sinal"] += list((v["acum12_passado"] > 0).astype(int))
        prev["media"] += [t["alvo_acum_12m"].mean()] * len(v)
        prev["persistencia"] += list(v["acum12_passado"])
    return [
        ("classificacao", "baseline_maioria", "", nota_classificacao(reais_c, prev["maioria"])),
        ("classificacao", "baseline_persistencia_sinal", "", nota_classificacao(reais_c, prev["persistencia_sinal"])),
        ("regressao", "baseline_media", "", nota_regressao(reais_r, prev["media"])),
        ("regressao", "baseline_persistencia", "", nota_regressao(reais_r, prev["persistencia"])),
    ]


def criar_pipeline(modelo, params):
    """Padronização + modelo; a padronização é ajustada só nos dados de treino de cada divisão."""
    if modelo == "logistica":
        estimador = LogisticRegression(C=params["C"], class_weight="balanced", max_iter=1000,
                                       random_state=config.SEMENTE)
    elif modelo == "ridge":
        estimador = Ridge(alpha=params["alpha"])
    elif modelo == "rf_classificacao":
        estimador = RandomForestClassifier(n_estimators=config.GRADE_RF_N_ESTIMATORS, class_weight="balanced",
                                           max_depth=params["max_depth"],
                                           min_samples_leaf=params["min_samples_leaf"],
                                           random_state=config.SEMENTE)
    else:
        estimador = RandomForestRegressor(n_estimators=config.GRADE_RF_N_ESTIMATORS,
                                          max_depth=params["max_depth"],
                                          min_samples_leaf=params["min_samples_leaf"],
                                          random_state=config.SEMENTE)
    return Pipeline([("padronizar", StandardScaler()), ("modelo", estimador)])


def nota_configuracao(treino, divisoes, modelo, params):
    """Ajusta em cada divisão, junta as previsões de validação e calcula uma nota única."""
    classificacao = modelo in ("logistica", "rf_classificacao")
    alvo = "alvo_alta" if classificacao else "alvo_acum_12m"
    reais, previsoes = [], []
    for idx_treino, idx_val in divisoes:
        t, v = treino.iloc[idx_treino], treino.iloc[idx_val]
        pipe = criar_pipeline(modelo, params)
        pipe.fit(t[config.FEATURES_MODELO], t[alvo])
        reais += list(v[alvo])
        previsoes += list(pipe.predict(v[config.FEATURES_MODELO]))
    return nota_classificacao(reais, previsoes) if classificacao else nota_regressao(reais, previsoes)


def escolher(notas, classificacao):
    """Lista ordenada do mais simples ao mais complexo: pega a primeira dentro da tolerância da melhor."""
    if classificacao:
        limite = max(notas) - config.TOLERANCIA_MACRO_F1
        return next(i for i, n in enumerate(notas) if n >= limite)
    limite = min(notas) * (1 + config.TOLERANCIA_RMSE)
    return next(i for i, n in enumerate(notas) if n <= limite)


def ajustar_modelo(treino, divisoes, modelo, grade):
    """Testa a grade, escolhe pela regra de desempate e devolve (linhas da tabela, escolhida, pipeline final)."""
    classificacao = modelo in ("logistica", "rf_classificacao")
    notas = [nota_configuracao(treino, divisoes, modelo, p) for p in grade]
    escolhida = escolher(notas, classificacao)
    tarefa = "classificacao" if classificacao else "regressao"
    linhas = [(tarefa, modelo, str(p), n, "sim" if i == escolhida else "") for i, (p, n) in enumerate(zip(grade, notas))]
    alvo = "alvo_alta" if classificacao else "alvo_acum_12m"
    final = criar_pipeline(modelo, grade[escolhida])
    final.fit(treino[config.FEATURES_MODELO], treino[alvo])
    return linhas, grade[escolhida], final


def main():
    treino = pd.read_csv(config.DADOS_PROCESSADOS / "modelagem_treino.csv", parse_dates=["mes"])
    if len(treino) != config.TAMANHOS_ESPERADOS[0]:
        parar(f"o treino deveria ter {config.TAMANHOS_ESPERADOS[0]} linhas e tem {len(treino)}")
    print(f"Treino lido: {len(treino)} linhas ({treino['mes'].min():%Y-%m} a {treino['mes'].max():%Y-%m})")

    divisoes = list(TimeSeriesSplit(n_splits=config.N_SPLITS_CV, test_size=config.TAMANHO_VALIDACAO_CV,
                                    gap=config.GAP_MESES).split(treino))
    mostrar_divisoes(treino, divisoes)

    print("\nBaselines (nota agrupada da validação; classificação = macro-F1, regressão = RMSE):")
    conferir_escala(treino)
    linhas = [(t, m, h, n, "baseline") for t, m, h, n in notas_baselines(treino, divisoes)]
    for tarefa, modelo, _, nota, _ in linhas:
        print(f"  {tarefa:13s} {modelo:28s} {nota:.4f}")

    grades = {
        "logistica": [{"C": c} for c in config.GRADE_LOGISTICA_C],
        "ridge": [{"alpha": a} for a in config.GRADE_RIDGE_ALPHA],
    }
    grade_rf = [{"max_depth": d, "min_samples_leaf": m}
                for d in config.GRADE_RF_MAX_DEPTH for m in config.GRADE_RF_MIN_SAMPLES_LEAF]
    grades["rf_classificacao"] = grade_rf
    grades["rf_regressao"] = grade_rf

    escolhidas, finais = [], {}
    for modelo, grade in grades.items():
        novas, escolhida, final = ajustar_modelo(treino, divisoes, modelo, grade)
        linhas += novas
        peso = "balanced" if modelo in ("logistica", "rf_classificacao") else ""
        escolhidas.append((novas[0][0], modelo, str(escolhida), peso))
        finais[modelo] = final
        unidade = "macro-F1" if novas[0][0] == "classificacao" else "RMSE"
        print(f"\n{modelo} ({unidade}, nota agrupada):")
        for _, _, params, nota, marca in novas:
            print(f"  {params:45s} {nota:.4f} {'<- escolhida' if marca else ''}")

    tabela = pd.DataFrame(linhas, columns=["tarefa", "modelo", "hiperparametros", "nota", "escolhida"])
    tabela.to_csv(config.TABELAS / "validacao_cruzada.csv", index=False)
    pd.DataFrame(escolhidas, columns=["tarefa", "modelo", "hiperparametros", "class_weight"]).to_csv(
        config.TABELAS / "hiperparametros_escolhidos.csv", index=False)

    # O 10 usa estes valores dos baselines (calculados nas 72 linhas do treino) e os 4 pipelines finais
    baselines = {"classe_majoritaria": int(treino["alvo_alta"].mean() >= 0.5),
                 "media_alvo": float(treino["alvo_acum_12m"].mean())}
    joblib.dump({"pipelines": finais, "baselines": baselines}, config.DADOS_PROCESSADOS / "modelos_treinados.joblib")
    print(f"\nBaselines do treino inteiro: classe majoritária = {baselines['classe_majoritaria']}, "
          f"média do alvo = {baselines['media_alvo']:.2f}")
    print("Gravados: validacao_cruzada.csv, hiperparametros_escolhidos.csv e modelos_treinados.joblib")


if __name__ == "__main__":
    main()
