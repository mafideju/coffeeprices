"""Baixa a variação mensal do IPCA do café moído a partir dos links da API do SIDRA."""
import pandas as pd
import requests

import config


def baixar_tabela_sidra(url):
    resposta = requests.get(url, timeout=120)
    resposta.raise_for_status()
    linhas = resposta.json()
    cabecalho = linhas[0]          # a primeira linha descreve as colunas
    tabela = pd.DataFrame(linhas[1:])

    chave_mes = next((k for k, v in cabecalho.items() if v == "Mês (Código)"), None)
    if chave_mes is None:
        raise SystemExit(f"Não achei a coluna do mês. Cabeçalho recebido: {cabecalho}")

    print("  Colunas com poucos valores distintos (confira se é café moído e variação mensal):")
    for chave, nome in cabecalho.items():
        if chave.startswith("D") and chave.endswith("N"):
            valores = tabela[chave].unique()
            if len(valores) <= 5:
                print(f"    {nome}: {list(valores)}")

    resultado = pd.DataFrame({
        "mes": pd.to_datetime(tabela[chave_mes], format="%Y%m"),
        "variacao_mensal": pd.to_numeric(tabela["V"], errors="coerce"),
    })
    if resultado["mes"].duplicated().any():
        raise SystemExit("Há meses repetidos: a consulta tem mais de uma categoria ou variável. "
                         "Refaça o link no SIDRA com só 'café moído' e só 'variação mensal'.")
    return resultado


def main():
    if not config.URLS_IPCA_CAFE:
        raise SystemExit("Preencha URLS_IPCA_CAFE em src/config.py (README, passo 2).")

    partes = []
    for i, url in enumerate(config.URLS_IPCA_CAFE, start=1):
        print(f"Baixando link {i}...")
        partes.append(baixar_tabela_sidra(url))

    ipca = pd.concat(partes).drop_duplicates("mes", keep="last").sort_values("mes")

    esperado = pd.date_range(ipca["mes"].min(), ipca["mes"].max(), freq="MS")
    faltando = esperado.difference(ipca["mes"])
    print(f"\nPeríodo: {ipca['mes'].min():%Y-%m} a {ipca['mes'].max():%Y-%m} ({len(ipca)} meses)")
    print(f"Meses faltando: {list(faltando.strftime('%Y-%m')) if len(faltando) else 'nenhum'}")
    print(f"Valores ausentes: {int(ipca['variacao_mensal'].isna().sum())}")

    saida = config.DADOS_BRUTOS / "ipca_cafe_moido.csv"
    ipca.to_csv(saida, index=False)
    print(f"Salvo em {saida}")


if __name__ == "__main__":
    main()
