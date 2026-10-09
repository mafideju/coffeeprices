"""Baixa chuva e temperatura mínima mensais (NASA POWER) para pontos de regiões cafeeiras."""
import time

import numpy as np
import pandas as pd
import requests

import config

URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"


def baixar_ponto(nome, latitude, longitude):
    parametros = {
        "start": config.ANO_COLETA_INICIO,
        "end": config.ANO_FIM,
        "latitude": latitude,
        "longitude": longitude,
        "community": "ag",
        "parameters": "PRECTOTCORR,T2M_MIN",
        "format": "json",
    }
    resposta = requests.get(URL, params=parametros, timeout=120)
    resposta.raise_for_status()
    dados = resposta.json()["properties"]["parameter"]

    linhas = []
    for variavel, serie in dados.items():
        for chave, valor in serie.items():
            if chave.endswith("13"):      # o mês 13 é a média anual: ignorar
                continue
            linhas.append({"ponto": nome, "mes": pd.to_datetime(chave, format="%Y%m"),
                           "variavel": variavel, "valor": valor})
    tabela = pd.DataFrame(linhas)
    tabela["valor"] = tabela["valor"].replace(-999, np.nan)   # -999 = dado ausente
    return tabela.pivot_table(index=["ponto", "mes"], columns="variavel", values="valor").reset_index()


def main():
    partes = []
    for nome, (lat, lon) in config.PONTOS_CLIMA.items():
        print(f"Baixando {nome}...")
        partes.append(baixar_ponto(nome, lat, lon))
        time.sleep(1)   # gentileza com a API

    pontos = pd.concat(partes).rename(columns={"PRECTOTCORR": "chuva_mm_dia",
                                              "T2M_MIN": "temp_min_c"})
    pontos.to_csv(config.DADOS_BRUTOS / "clima_pontos.csv", index=False)

    # Índice nacional simples: média dos pontos em cada mês
    regioes = pontos.groupby("mes", as_index=False)[["chuva_mm_dia", "temp_min_c"]].mean()
    regioes.to_csv(config.DADOS_BRUTOS / "clima_regioes.csv", index=False)
    print(regioes.tail(3))
    print(f"Valores ausentes: {int(regioes[['chuva_mm_dia', 'temp_min_c']].isna().sum().sum())}")


if __name__ == "__main__":
    main()
