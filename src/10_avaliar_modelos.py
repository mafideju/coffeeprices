"""Avalia os modelos no teste (único ponto do projeto que lê o teste), gera tabelas e figuras."""
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (balanced_accuracy_score, confusion_matrix, f1_score,
                             mean_absolute_error, mean_squared_error)

import config

AVISO = "resultados indicativos: teste com 33 linhas (cerca de 3 janelas independentes)"


def main():
    teste = pd.read_csv(config.DADOS_PROCESSADOS / "modelagem_teste.csv", parse_dates=["mes"])
    if len(teste) != config.TAMANHOS_ESPERADOS[1]:
        print(f"ERRO: o teste deveria ter {config.TAMANHOS_ESPERADOS[1]} linhas e tem {len(teste)}")
        sys.exit(1)
    salvo = joblib.load(config.DADOS_PROCESSADOS / "modelos_treinados.joblib")
    pipes, base = salvo["pipelines"], salvo["baselines"]
    X = teste[config.FEATURES_MODELO]
    y_alta, y_acum = teste["alvo_alta"], teste["alvo_acum_12m"]
    print(f"Teste: {len(teste)} linhas ({teste['mes'].min():%Y-%m} a {teste['mes'].max():%Y-%m})")
    print(f"AVISO: {AVISO}\n")

    # Previsões de cada modelo (os baselines usam só o treino e acum12_passado)
    prev_c = {
        "baseline_maioria": np.full(len(teste), base["classe_majoritaria"]),
        "baseline_persistencia_sinal": (teste["acum12_passado"] > 0).astype(int).to_numpy(),
        "logistica": pipes["logistica"].predict(X),
        "rf_classificacao": pipes["rf_classificacao"].predict(X),
    }
    prev_r = {
        "baseline_media": np.full(len(teste), base["media_alvo"]),
        "baseline_persistencia": teste["acum12_passado"].to_numpy(),
        "ridge": pipes["ridge"].predict(X),
        "rf_regressao": pipes["rf_regressao"].predict(X),
    }

    linhas = []
    for modelo, p in prev_c.items():
        vn, fp, fn, vp = confusion_matrix(y_alta, p, labels=[0, 1]).ravel()
        linhas.append({"modelo": modelo,
                       "macro_f1": f1_score(y_alta, p, average="macro", labels=[0, 1], zero_division=0),
                       "acuracia_balanceada": balanced_accuracy_score(y_alta, p),
                       "VN": vn, "FP": fp, "FN": fn, "VP": vp, "n_teste": len(teste)})
    met_c = pd.DataFrame(linhas)
    met_c.to_csv(config.TABELAS / "metricas_classificacao.csv", index=False)

    linhas = []
    for modelo, p in prev_r.items():
        linhas.append({"modelo": modelo,
                       "rmse": float(np.sqrt(mean_squared_error(y_acum, p))),
                       "mae": mean_absolute_error(y_acum, p), "n_teste": len(teste)})
    met_r = pd.DataFrame(linhas)
    met_r.to_csv(config.TABELAS / "metricas_regressao.csv", index=False)

    previsoes = teste[["mes", "alvo_alta", "alvo_acum_12m"]].copy()
    for modelo, p in {**prev_c, **prev_r}.items():
        previsoes[modelo] = p
    previsoes.to_csv(config.TABELAS / "previsoes_teste.csv", index=False)

    print("Classificação (teste):")
    print(met_c.round(4).to_string(index=False))
    print("\nRegressão (teste):")
    print(met_r.round(4).to_string(index=False))

    importancia = calcular_importancia(pipes)
    importancia.to_csv(config.TABELAS / "importancia_variaveis.csv", index=False)
    print("\nImportância das variáveis (coeficientes padronizados da logística e do Ridge; "
          "importância do Random Forest), ordenada por |valor|:")
    for (tarefa, modelo), g in importancia.groupby(["tarefa", "modelo"], sort=False):
        print(f"  {tarefa} / {modelo}:")
        for _, r in g.reindex(g["valor"].abs().sort_values(ascending=False).index).iterrows():
            print(f"    {r['variavel']:24s} {r['valor']:+.4f}")


def calcular_importancia(pipes):
    """Coeficientes (já padronizados, pois o Pipeline padroniza antes) e importância do Random Forest."""
    partes = []
    for modelo, tarefa in [("logistica", "classificacao"), ("ridge", "regressao"),
                           ("rf_classificacao", "classificacao"), ("rf_regressao", "regressao")]:
        estimador = pipes[modelo].named_steps["modelo"]
        valores = estimador.coef_.ravel() if hasattr(estimador, "coef_") else estimador.feature_importances_
        partes.append(pd.DataFrame({"tarefa": tarefa, "modelo": modelo,
                                    "variavel": config.FEATURES_MODELO, "valor": valores}))
    return pd.concat(partes, ignore_index=True)


if __name__ == "__main__":
    main()
