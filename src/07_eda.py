"""Análise exploratória (EDA): estatísticas, qualidade, outliers, correlações e gráficos."""
import matplotlib
matplotlib.use("Agg")   # salva as figuras em arquivo, sem abrir janelas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config

BASE = ["variacao_mensal", "acum12_passado", "cambio_medio", "arabica_usd_kg",
        "chuva_anom", "tempmin_anom", "oni", "alvo_acum_12m"]
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def salvar(nome):
    plt.tight_layout()
    plt.savefig(config.FIGURAS / nome, dpi=150)
    plt.close()
    print(f"  figura: {nome}")


def main():
    df = pd.read_csv(config.DADOS_PROCESSADOS / "dataset_mensal.csv", parse_dates=["mes"])
    base = [c for c in BASE if c in df.columns]

    # --- Estatísticas e qualidade (seções 10, 12 e 15) ---
    print(f"Registros: {len(df)} | Variáveis: {df.shape[1]} | Período: {df['mes'].min():%Y-%m} a {df['mes'].max():%Y-%m}")
    print(f"Meses duplicados: {int(df['mes'].duplicated().sum())}")
    df[base].describe().T.to_csv(config.TABELAS / "estatisticas_descritivas.csv")
    ausentes = df.isna().sum().rename("ausentes").to_frame()
    ausentes["percentual"] = (ausentes["ausentes"] / len(df) * 100).round(1)
    ausentes.to_csv(config.TABELAS / "valores_ausentes.csv")
    print("Ausentes nas variáveis-base:")
    print(ausentes.loc[base].to_string())

    # --- Outliers (seção 14): IQR e Z-score ---
    linhas = []
    for coluna in base:
        serie = df[coluna].dropna()
        q1, q3 = serie.quantile([0.25, 0.75])
        iqr = q3 - q1
        fora_iqr = ((serie < q1 - 1.5 * iqr) | (serie > q3 + 1.5 * iqr)).sum()
        fora_z = ((serie - serie.mean()).abs() / serie.std() > 3).sum()
        linhas.append({"variavel": coluna, "outliers_iqr": int(fora_iqr), "outliers_z3": int(fora_z)})
    pd.DataFrame(linhas).to_csv(config.TABELAS / "outliers.csv", index=False)
    print("Outliers (IQR e Z>3):")
    print(pd.DataFrame(linhas).to_string(index=False))

    # --- Balanceamento do alvo (seções 13 e 16) ---
    balanco = df["alvo_alta"].value_counts(dropna=True)
    print(f"Classes do alvo (1=alta): {balanco.to_dict()}")

    # --- Correlações (seção 15) ---
    corr = df[base].corr()
    corr.to_csv(config.TABELAS / "matriz_correlacao.csv")
    colunas_lag = [c for c in df.columns if "_l" in c and c.split("_l")[-1].isdigit()]
    corr_alvo = df[colunas_lag + ["acum12_passado"]].corrwith(df["alvo_acum_12m"]).dropna()
    corr_alvo = corr_alvo.reindex(corr_alvo.abs().sort_values(ascending=False).index)
    corr_alvo.rename("correlacao_com_alvo").to_csv(config.TABELAS / "correlacao_com_alvo.csv")
    # Só treino, sem as linhas cujo alvo invade o teste (evita escolher variáveis olhando o teste)
    ultimo_mes = pd.Timestamp(f"{config.ANO_FIM_TREINO}-12-01") - pd.DateOffset(months=config.GAP_MESES)
    treino = df[(df["mes"] <= ultimo_mes) & df["alvo_acum_12m"].notna()]
    corr_treino = treino[config.FEATURES_CANDIDATAS].corrwith(treino["alvo_acum_12m"]).dropna()
    corr_treino = corr_treino.reindex(corr_treino.abs().sort_values(ascending=False).index)
    corr_treino.rename("correlacao_com_alvo").to_csv(config.TABELAS / "correlacao_com_alvo_treino.csv")
    print(f"Correlações só no treino ({len(treino)} linhas, até {ultimo_mes:%Y-%m}), maiores 8:")
    print(corr_treino.head(8).round(2).to_string())
    print("Maiores correlações com o alvo (atenção: janelas de 12 meses se sobrepõem e inflam a correlação):")
    print(corr_alvo.head(8).round(2).to_string())

    # --- Gráficos ---
    print("Gráficos:")
    plt.figure(figsize=(10, 4))
    plt.plot(df["mes"], df["variacao_mensal"])
    plt.axhline(0, color="gray", lw=0.8)
    plt.title("IPCA café moído: variação mensal (%)")
    salvar("01_variacao_mensal.png")

    plt.figure(figsize=(10, 4))
    plt.plot(df["mes"], df["acum12_passado"])
    plt.axhline(0, color="gray", lw=0.8)
    plt.title("IPCA café moído: variação acumulada em 12 meses (%)")
    salvar("02_acumulada_12m.png")

    plt.figure(figsize=(6, 4))
    plt.hist(df["variacao_mensal"].dropna(), bins=20, edgecolor="black")
    plt.title("Distribuição da variação mensal (%)")
    salvar("03_histograma_variacao.png")

    plt.figure(figsize=(9, 4))
    plt.boxplot([df.loc[df["mes_do_ano"] == m, "variacao_mensal"].dropna() for m in range(1, 13)])
    plt.xticks(range(1, 13), MESES)
    plt.title("Variação mensal por mês do ano (sazonalidade)")
    salvar("04_boxplot_sazonalidade.png")

    series = [("cambio_medio", "Câmbio médio (R$/US$)"), ("arabica_usd_kg", "Arábica (US$/kg)"),
              ("chuva_anom", "Anomalia de chuva (mm/dia)"), ("tempmin_anom", "Anomalia de temp. mínima (°C)"),
              ("oni", "ONI (El Niño/La Niña)")]
    series = [s for s in series if s[0] in df.columns]
    fig, eixos = plt.subplots(len(series), 1, figsize=(10, 2.2 * len(series)), sharex=True)
    for eixo, (coluna, titulo) in zip(np.atleast_1d(eixos), series):
        eixo.plot(df["mes"], df[coluna])
        eixo.set_title(titulo, fontsize=9)
    salvar("05_variaveis_explicativas.png")

    plt.figure(figsize=(7, 6))
    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.xticks(range(len(base)), base, rotation=60, ha="right")
    plt.yticks(range(len(base)), base)
    for i in range(len(base)):
        for j in range(len(base)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=7)
    plt.colorbar()
    plt.title("Matriz de correlação")
    salvar("06_matriz_correlacao.png")

    top = corr_alvo.head(15).iloc[::-1]
    plt.figure(figsize=(8, 5))
    plt.barh(top.index, top.values)
    plt.title("Maiores correlações com o alvo (12 meses à frente)")
    salvar("07_correlacao_lags_alvo.png")

    plt.figure(figsize=(10, 4))
    plt.plot(df["mes"], df["alvo_acum_12m"])
    plt.axhline(0, color="gray", lw=0.8)
    plt.axvline(pd.Timestamp(f"{config.ANO_FIM_TREINO + 1}-01-01"), color="red", ls="--", label="início do teste")
    plt.legend()
    plt.title("Alvo: variação acumulada nos 12 meses seguintes (%)")
    salvar("08_alvo_e_divisao_treino_teste.png")

    print(f"\nTabelas em {config.TABELAS}\nFiguras em {config.FIGURAS}")


if __name__ == "__main__":
    main()
