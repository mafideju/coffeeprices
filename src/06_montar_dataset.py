"""Junta todas as fontes, cria as variáveis (defasagens, anomalias) e o alvo de 12 meses."""
import numpy as np
import pandas as pd

import config

# Defasagens (em meses) que serão criadas para cada variável. 0 = valor do próprio mês.
LAGS = {
    "variacao_mensal": [0, 1, 3, 6, 12],
    "cambio_medio": [0, 3, 6, 12],
    "arabica_usd_kg": [0, 3, 6, 12],
    "chuva_anom": [0, 3, 6, 9, 12],
    "tempmin_anom": [0, 3, 6, 9, 12],
    "oni": [2, 6, 12],   # o ONI é revisado por até 2 meses: nunca usamos o valor do mês atual
}


def ler_csv(nome):
    caminho = config.DADOS_BRUTOS / nome
    if not caminho.exists():
        raise SystemExit(f"Arquivo não encontrado: {caminho}. Rode antes o script que o gera.")
    return pd.read_csv(caminho, parse_dates=["mes"])


def main():
    # 1) Junção das fontes (o IPCA é a tabela principal)
    df = ler_csv("ipca_cafe_moido.csv")
    for nome in ["cambio.csv", "clima_regioes.csv", "oni.csv", "arabica.csv"]:
        df = df.merge(ler_csv(nome), on="mes", how="left")
    df = df.sort_values("mes").set_index("mes").asfreq("MS")   # garante 1 linha por mês

    # 2) Sazonalidade
    df["mes_do_ano"] = df.index.month
    df["mes_sen"] = np.sin(2 * np.pi * df["mes_do_ano"] / 12)
    df["mes_cos"] = np.cos(2 * np.pi * df["mes_do_ano"] / 12)

    # 3) Anomalias climáticas: desvio em relação à média do mesmo mês no período de TREINO
    base = df[df.index.year <= config.ANO_FIM_TREINO]
    for original, anomalia in [("chuva_mm_dia", "chuva_anom"), ("temp_min_c", "tempmin_anom")]:
        media_do_mes = base.groupby("mes_do_ano")[original].mean()
        df[anomalia] = df[original] - df["mes_do_ano"].map(media_do_mes)

    # 4) Variáveis do passado do próprio IPCA e alvo (futuro)
    fator = 1 + df["variacao_mensal"] / 100
    produto_12 = fator.rolling(12).apply(np.prod, raw=True)
    df["acum3_passado"] = (fator.rolling(3).apply(np.prod, raw=True) - 1) * 100
    df["acum12_passado"] = (produto_12 - 1) * 100
    # Alvo: variação acumulada de t+1 até t+12 (produto_12 em t+12 cobre exatamente esse intervalo)
    df["alvo_acum_12m"] = (produto_12.shift(-12) - 1) * 100
    df["alvo_alta"] = (df["alvo_acum_12m"] > 0).astype(float).where(df["alvo_acum_12m"].notna())

    # 5) Defasagens
    for coluna, lags in LAGS.items():
        for lag in lags:
            df[f"{coluna}_l{lag}"] = df[coluna].shift(lag)

    # 5b) Variações percentuais (em %) de câmbio e arábica: usam só o passado
    for coluna in ["cambio_medio", "arabica_usd_kg"]:
        for meses in [3, 6, 12]:
            df[f"{coluna}_var{meses}m"] = df[coluna].pct_change(meses) * 100

    # 6) Safra (opcional): usa a safra do ANO ANTERIOR para não usar informação futura
    arquivo_safra = config.DADOS_BRUTOS / "safra_conab.csv"
    df = df.reset_index()
    if arquivo_safra.exists():
        safra = pd.read_csv(arquivo_safra)
        safra["bienal_positiva"] = safra["bienalidade"].str.lower().str.startswith("pos").astype(int)
        safra["ano"] = safra["ano"] + 1
        safra = safra.rename(columns={"producao_milhoes_sacas": "safra_anterior_milhoes_sacas",
                                      "bienal_positiva": "safra_anterior_bienal_positiva"})
        df["ano"] = df["mes"].dt.year
        df = df.merge(safra[["ano", "safra_anterior_milhoes_sacas", "safra_anterior_bienal_positiva"]],
                      on="ano", how="left").drop(columns="ano")
    else:
        print("Aviso: dados/brutos/safra_conab.csv não existe; seguindo sem as variáveis de safra.")

    # 7) Recorte final e marcação treino/teste
    df = df[df["mes"] >= f"{config.ANO_INICIO}-01-01"].copy()
    df["periodo"] = np.where(df["mes"].dt.year <= config.ANO_FIM_TREINO, "treino", "teste")

    saida = config.DADOS_PROCESSADOS / "dataset_mensal.csv"
    df.to_csv(saida, index=False)

    print(f"Dataset: {df.shape[0]} linhas x {df.shape[1]} colunas, {df['mes'].min():%Y-%m} a {df['mes'].max():%Y-%m}")
    print(f"Linhas com alvo disponível: {int(df['alvo_acum_12m'].notna().sum())}")
    print("Distribuição do alvo de classificação (1 = alta):")
    print(df["alvo_alta"].value_counts(dropna=True).to_string())
    print(f"Salvo em {saida}")


if __name__ == "__main__":
    main()
