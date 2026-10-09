"""Lê o preço mensal do café arábica da planilha 'Pink Sheet' do Banco Mundial (download manual)."""
import pandas as pd

import config


def main():
    arquivos = sorted(config.DADOS_BRUTOS.glob("*.xls*"))
    if not arquivos:
        raise SystemExit("Coloque a planilha mensal do Banco Mundial (Pink Sheet) em dados/brutos/ "
                         "(README, passo 3).")
    arquivo = arquivos[0]
    print(f"Lendo {arquivo.name}")

    bruto = pd.read_excel(arquivo, sheet_name="Monthly Prices", header=None)

    # Acha a coluna "Coffee, Arabica" nas primeiras linhas (cabeçalho)
    cabecalho = bruto.iloc[:10].astype(str).apply(lambda col: col.str.strip())
    achou = cabecalho.eq("Coffee, Arabica")
    if not achou.any().any():
        print(bruto.head(8))
        raise SystemExit("Não achei 'Coffee, Arabica'. Confira a planilha acima.")
    coluna = achou.any().idxmax()

    # As datas aparecem como 2016M01, 2016M02...
    datas = bruto[0].astype(str).str.strip()
    linhas = datas.str.match(r"^\d{4}M\d{2}$")
    arabica = pd.DataFrame({
        "mes": pd.to_datetime(datas[linhas], format="%YM%m"),
        "arabica_usd_kg": pd.to_numeric(bruto.loc[linhas, coluna], errors="coerce"),
    })
    arabica = arabica[arabica["mes"].dt.year >= config.ANO_COLETA_INICIO]

    print(arabica.tail(3))
    arabica.to_csv(config.DADOS_BRUTOS / "arabica.csv", index=False)
    print(f"{len(arabica)} meses salvos")


if __name__ == "__main__":
    main()
