"""Baixa o câmbio (média mensal) da API de dados abertos do Banco Central."""
from datetime import date

import pandas as pd
import requests

import config


def main():
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{config.SGS_CAMBIO}/dados"
    parametros = {
        "formato": "json",
        "dataInicial": f"01/01/{config.ANO_COLETA_INICIO}",
        "dataFinal": date.today().strftime("%d/%m/%Y"),
    }
    resposta = requests.get(url, params=parametros, timeout=60)
    resposta.raise_for_status()

    cambio = pd.DataFrame(resposta.json())
    cambio["mes"] = (pd.to_datetime(cambio["data"], format="%d/%m/%Y")
                     .dt.to_period("M").dt.to_timestamp())
    cambio["cambio_medio"] = pd.to_numeric(cambio["valor"], errors="coerce")
    # Se a série for diária, esta média mensal também funciona.
    cambio = cambio.groupby("mes", as_index=False)["cambio_medio"].mean()

    print(cambio.head(3))
    print(cambio.tail(3))
    saida = config.DADOS_BRUTOS / "cambio.csv"
    cambio.to_csv(saida, index=False)
    print(f"{len(cambio)} meses salvos em {saida}")


if __name__ == "__main__":
    main()
