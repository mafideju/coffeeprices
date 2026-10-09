"""Baixa o índice ENSO (ONI) publicado pela NOAA."""
import io

import pandas as pd
import requests

import config

URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
# Cada trimestre móvel é associado ao seu mês central.
MES_CENTRAL = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6,
               "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}


def main():
    resposta = requests.get(URL, timeout=60)
    resposta.raise_for_status()
    oni = pd.read_csv(io.StringIO(resposta.text), sep=r"\s+")   # colunas: SEAS YR TOTAL ANOM

    oni["mes"] = pd.to_datetime({"year": oni["YR"], "month": oni["SEAS"].map(MES_CENTRAL), "day": 1})
    oni = oni.rename(columns={"ANOM": "oni"})[["mes", "oni"]]
    oni = oni[oni["mes"].dt.year >= config.ANO_COLETA_INICIO]

    print(oni.tail(3))
    oni.to_csv(config.DADOS_BRUTOS / "oni.csv", index=False)
    print(f"{len(oni)} meses salvos")


if __name__ == "__main__":
    main()
