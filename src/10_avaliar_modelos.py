"""Avalia os modelos no teste (único ponto do projeto que lê o teste), gera tabelas e figuras."""
import sys

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

    figura_comparacao(met_c, met_r)
    figura_matrizes(met_c)
    figura_previsto_vs_real(previsoes)
    figura_importancia(importancia)
    print(f"\nFiguras gravadas em {config.FIGURAS}: 09_comparacao_modelos.png, 10_matrizes_confusao.png, "
          "11_previsto_vs_real.png, 12_importancia_variaveis.png")


def figura_previsto_vs_real(previsoes):
    """Regressão: real contra a previsão de cada modelo, mês a mês no teste."""
    fig, eixo = plt.subplots(figsize=(12, 5))
    eixo.plot(previsoes["mes"], previsoes["alvo_acum_12m"], color="black", linewidth=2.5, label="real")
    estilos = {"baseline_media": ("#9e9e9e", "--"), "baseline_persistencia": ("#bdbdbd", ":"),
               "ridge": ("#1f77b4", "-"), "rf_regressao": ("#d62728", "-")}
    for modelo, (cor, estilo) in estilos.items():
        eixo.plot(previsoes["mes"], previsoes[modelo], color=cor, linestyle=estilo, label=modelo)
    eixo.axhline(0, color="black", linewidth=0.5)
    eixo.set_ylabel("variação acumulada do IPCA do café nos 12 meses seguintes (%)")
    eixo.set_title(f"Previsto contra real no teste (regressão) - {AVISO}", fontsize=10)
    eixo.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "11_previsto_vs_real.png", dpi=150)
    plt.close(fig)


def figura_importancia(importancia):
    """Coeficientes padronizados (modelos lineares) e importância do Random Forest, por modelo."""
    fig, eixos = plt.subplots(1, 4, figsize=(17, 6), sharey=True)
    ordem = (importancia[importancia["modelo"] == "rf_classificacao"]
             .sort_values("valor")["variavel"].tolist())
    for eixo, (modelo, g) in zip(eixos, importancia.groupby("modelo", sort=False)):
        g = g.set_index("variavel").loc[ordem]
        cores = ["#d62728" if v < 0 else "#1f77b4" for v in g["valor"]]
        eixo.barh(g.index, g["valor"], color=cores)
        eixo.axvline(0, color="black", linewidth=0.5)
        tipo = "coeficiente padronizado" if modelo in ("logistica", "ridge") else "importância"
        eixo.set_title(f"{modelo}\n({tipo})", fontsize=9)
    fig.suptitle(f"Importância das variáveis - {AVISO}", fontsize=11)
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "12_importancia_variaveis.png", dpi=150)
    plt.close(fig)


COR_BASELINE, COR_MODELO = "#9e9e9e", "#1f77b4"


def figura_comparacao(met_c, met_r):
    """Barras: macro-F1 e acurácia balanceada (classificação); RMSE e MAE (regressão)."""
    fig, eixos = plt.subplots(2, 2, figsize=(13, 8))
    for eixo, tabela, coluna, titulo in [
        (eixos[0, 0], met_c, "macro_f1", "Classificação: macro-F1 (maior é melhor)"),
        (eixos[0, 1], met_c, "acuracia_balanceada", "Classificação: acurácia balanceada (maior é melhor)"),
        (eixos[1, 0], met_r, "rmse", "Regressão: RMSE em p.p. (menor é melhor)"),
        (eixos[1, 1], met_r, "mae", "Regressão: MAE em p.p. (menor é melhor)"),
    ]:
        cores = [COR_BASELINE if m.startswith("baseline") else COR_MODELO for m in tabela["modelo"]]
        eixo.bar(tabela["modelo"], tabela[coluna], color=cores)
        for i, v in enumerate(tabela[coluna]):
            eixo.text(i, v, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
        eixo.set_title(titulo, fontsize=10)
        eixo.tick_params(axis="x", rotation=25, labelsize=8)
    fig.suptitle(f"Modelos contra baselines (cinza = baseline) - {AVISO}", fontsize=11)
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "09_comparacao_modelos.png", dpi=150)
    plt.close(fig)


def figura_matrizes(met_c):
    """Uma matriz de confusão por modelo de classificação (linha = real, coluna = previsto)."""
    fig, eixos = plt.subplots(1, 4, figsize=(15, 4))
    for eixo, (_, r) in zip(eixos, met_c.iterrows()):
        matriz = np.array([[r["VN"], r["FP"]], [r["FN"], r["VP"]]])
        eixo.imshow(matriz, cmap="Blues")
        for i in range(2):
            for j in range(2):
                eixo.text(j, i, int(matriz[i, j]), ha="center", va="center", fontsize=14,
                          color="white" if matriz[i, j] > matriz.max() / 2 else "black")
        eixo.set_xticks([0, 1], ["queda", "alta"])
        eixo.set_yticks([0, 1], ["queda", "alta"])
        eixo.set_xlabel("previsto")
        eixo.set_ylabel("real")
        eixo.set_title(r["modelo"], fontsize=9)
    fig.suptitle(f"Matrizes de confusão no teste - {AVISO}", fontsize=11)
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "10_matrizes_confusao.png", dpi=150)
    plt.close(fig)


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
