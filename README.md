# Projeto café: roteiro de coleta e EDA (CRISP-DM, etapas 1 e 2)

Scripts simples, executados um por vez, na ordem. Cada um gera arquivos que o próximo usa.
Os resultados reais da execução preenchem as seções 10 a 17 do relatório.

## Passo 1: preparar o ambiente no PyCharm (uma vez)

1. Abra a pasta `cafe-ml` no PyCharm (File > Open).
2. Crie um ambiente virtual com Python 3.12 (Settings > Project > Python Interpreter > Add Interpreter > Virtualenv).
3. No terminal do PyCharm: `pip install -r requirements.txt`
4. Rode os scripts sempre a partir da pasta raiz `cafe-ml`, por exemplo: `python src/01_coletar_ipca.py`

## Passo 2: gerar os links do IPCA no SIDRA (manual, 1 vez)

Não coloquei códigos de tabela e de categoria no código de propósito: confirme tudo você mesmo no SIDRA.

1. Acesse sidra.ibge.gov.br e abra a tabela 7060 (IPCA, de 2020 em diante).
2. Selecione: variável = variação mensal; categoria = o subitem **café moído**; território = Brasil; período = todos os meses.
3. Na tela de consulta, use a opção que gera o **link da API** e copie o endereço.
4. Repita para o período anterior (2015 a 2019): procure no SIDRA a tabela do IPCA que cubra esses anos, com o mesmo subitem e a mesma variável. Confirme o código dela e o período de cobertura.
5. Cole os dois links em `URLS_IPCA_CAFE` no arquivo `src/config.py`.
6. Os links devem cobrir **desde 2015** (precisamos de 1 ano extra para as defasagens).

## Passo 3: baixar a planilha do Banco Mundial (manual, 1 vez)

Em worldbank.org/en/research/commodity-markets, baixe a planilha mensal de preços (Pink Sheet, arquivo Excel) e salve em `dados/brutos/`.

## Passo 4 (opcional): dados de safra da CONAB

Crie `dados/brutos/safra_conab.csv` com as colunas `ano,producao_milhoes_sacas,bienalidade` (valor "positiva" ou "negativa"), preenchido a partir das publicações da CONAB (Acompanhamento da Safra Brasileira de Café), de 2015 em diante. Sem esse arquivo, o projeto roda sem as variáveis de safra.

## Ordem de execução

| Ordem | Script | O que faz | Seção do relatório |
|---|---|---|---|
| 1 | `01_coletar_ipca.py` | Baixa o IPCA do café moído e checa meses faltando | 9, 10, 12 |
| 2 | `02_coletar_cambio.py` | Baixa o câmbio mensal do Banco Central | 9, 10 |
| 3 | `03_coletar_clima.py` | Baixa chuva e temperatura mínima (NASA POWER) | 9, 10 |
| 4 | `04_coletar_oni.py` | Baixa o índice ENSO (NOAA) | 9, 10 |
| 5 | `05_ler_arabica.py` | Lê o arábica do Banco Mundial | 9, 10 |
| 6 | `06_montar_dataset.py` | Junta tudo, cria defasagens, anomalias e o alvo | 10, 11, 17 |
| 7 | `07_eda.py` | Estatísticas, ausentes, outliers, correlações, 8 gráficos | 12 a 16 |

Saídas: `dados/brutos/` (dados coletados), `dados/processados/dataset_mensal.csv`, `relatorio/tabelas/` (CSVs para o relatório) e `relatorio/figuras/` (gráficos PNG).

Author: db.mars@proton.me