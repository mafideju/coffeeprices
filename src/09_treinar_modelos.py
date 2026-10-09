"""Treina baselines, modelo linear e Random Forest usando SÓ o treino (o teste não é aberto aqui)."""
import sys

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

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


def main():
    treino = pd.read_csv(config.DADOS_PROCESSADOS / "modelagem_treino.csv", parse_dates=["mes"])
    if len(treino) != config.TAMANHOS_ESPERADOS[0]:
        parar(f"o treino deveria ter {config.TAMANHOS_ESPERADOS[0]} linhas e tem {len(treino)}")
    print(f"Treino lido: {len(treino)} linhas ({treino['mes'].min():%Y-%m} a {treino['mes'].max():%Y-%m})")

    divisoes = list(TimeSeriesSplit(n_splits=config.N_SPLITS_CV, test_size=config.TAMANHO_VALIDACAO_CV,
                                    gap=config.GAP_MESES).split(treino))
    mostrar_divisoes(treino, divisoes)


if __name__ == "__main__":
    main()
