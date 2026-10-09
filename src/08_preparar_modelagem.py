"""Monta o treino e o teste da modelagem (divisão temporal, sem embaralhar) e confere os tamanhos."""
import sys

import pandas as pd

import config

ALVOS = ["alvo_alta", "alvo_acum_12m"]


def parar(mensagem):
    print(f"ERRO: {mensagem}")
    sys.exit(1)


def main():
    df = pd.read_csv(config.DADOS_PROCESSADOS / "dataset_mensal.csv", parse_dates=["mes"])
    features = config.FEATURES_MODELO

    # Só as 13 variáveis fixas podem entrar (nada de oni sem defasagem, periodo, alvos ou colunas brutas)
    faltando = [c for c in features if c not in df.columns]
    if faltando:
        parar(f"colunas ausentes no dataset: {faltando}")
    proibidas = {"oni", "periodo", "chuva_mm_dia", "temp_min_c"} | set(ALVOS)
    if proibidas & set(features):
        parar(f"variáveis proibidas em FEATURES_MODELO: {sorted(proibidas & set(features))}")
    if len(features) != 13 or len(set(features)) != 13:
        parar(f"FEATURES_MODELO deve ter exatamente 13 variáveis distintas, tem {len(features)}")

    # Treino termina 12 meses antes do fim de 2022; o teste começa em 2023-01. 2022 é descartado.
    fim_treino = pd.Timestamp(f"{config.ANO_FIM_TREINO}-12-01") - pd.DateOffset(months=config.GAP_MESES)
    inicio_teste = pd.Timestamp(f"{config.ANO_FIM_TREINO + 1}-01-01")
    com_alvo = df[df["alvo_acum_12m"].notna()]
    treino = com_alvo[com_alvo["mes"] <= fim_treino]
    teste = com_alvo[com_alvo["mes"] >= inicio_teste]
    descartado = com_alvo[(com_alvo["mes"] > fim_treino) & (com_alvo["mes"] < inicio_teste)]

    colunas = ["mes"] + features + ALVOS
    treino = treino[colunas]
    teste = teste[colunas]

    print(f"Treino: {len(treino)} linhas ({treino['mes'].min():%Y-%m} a {treino['mes'].max():%Y-%m})")
    print(f"Descartado (intervalo de segurança): {len(descartado)} linhas "
          f"({descartado['mes'].min():%Y-%m} a {descartado['mes'].max():%Y-%m})")
    print(f"Teste: {len(teste)} linhas ({teste['mes'].min():%Y-%m} a {teste['mes'].max():%Y-%m})")
    print(f"Proporção de alta: treino {treino['alvo_alta'].mean():.0%} "
          f"({int(treino['alvo_alta'].sum())} de {len(treino)}), "
          f"teste {teste['alvo_alta'].mean():.0%} ({int(teste['alvo_alta'].sum())} de {len(teste)})")
    print(f"Variáveis do modelo ({len(features)}): {', '.join(features)}")
    nan_treino = int(treino[features].isna().sum().sum())
    nan_teste = int(teste[features].isna().sum().sum())
    print(f"NaN nas variáveis: treino {nan_treino}, teste {nan_teste}")

    if (len(treino), len(teste)) != config.TAMANHOS_ESPERADOS:
        parar(f"tamanhos esperados {config.TAMANHOS_ESPERADOS}, obtidos {(len(treino), len(teste))}")
    if nan_treino or nan_teste:
        parar("há valores ausentes nas variáveis do modelo")
    # O alvo da última linha do treino cobre os 12 meses seguintes: não pode alcançar o teste
    ultimo_alvo_coberto = treino["mes"].max() + pd.DateOffset(months=12)
    print(f"Último mês coberto pelo alvo do treino: {ultimo_alvo_coberto:%Y-%m} (teste começa em {teste['mes'].min():%Y-%m})")
    if ultimo_alvo_coberto >= teste["mes"].min():
        parar("o alvo do treino invade o teste (vazamento)")

    treino.to_csv(config.DADOS_PROCESSADOS / "modelagem_treino.csv", index=False)
    teste.to_csv(config.DADOS_PROCESSADOS / "modelagem_teste.csv", index=False)
    print("OK: gravados modelagem_treino.csv e modelagem_teste.csv em dados/processados/")


if __name__ == "__main__":
    main()
