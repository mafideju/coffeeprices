"""Configurações centrais do projeto. Edite aqui, e só aqui."""
from datetime import date
from pathlib import Path

# --- Pastas (criadas automaticamente) ---
RAIZ = Path(__file__).resolve().parent.parent
DADOS_BRUTOS = RAIZ / "dados" / "brutos"
DADOS_PROCESSADOS = RAIZ / "dados" / "processados"
FIGURAS = RAIZ / "relatorio" / "figuras"
TABELAS = RAIZ / "relatorio" / "tabelas"
for pasta in (DADOS_BRUTOS, DADOS_PROCESSADOS, FIGURAS, TABELAS):
    pasta.mkdir(parents=True, exist_ok=True)

# --- Período ---
ANO_INICIO = 2016                 # primeiro ano do dataset final
ANO_COLETA_INICIO = ANO_INICIO - 1  # coletamos 1 ano antes para calcular defasagens
ANO_FIM = date.today().year
ANO_FIM_TREINO = 2022             # treino: até este ano; teste: anos seguintes

# --- IPCA café moído (SIDRA) ---
# Cole aqui os links de API gerados no SIDRA (veja o README, passo 2).
# Use 2 links: um para o período antigo e outro para a tabela 7060 (2020 em diante).

# Série histórica: tabela 1419 (2015–2019).
# Série recente: tabela 7060 (2020 em diante).
URLS_IPCA_CAFE = [
    (
        "https://apisidra.ibge.gov.br/values/"
        "t/1419/n1/1/v/63/p/201501-201912/c315/7392"
    ),
    (
        "https://apisidra.ibge.gov.br/values/"
        "t/7060/n1/1/v/63/p/202001-202609/c315/7392"
    ),
]

# --- Câmbio (Banco Central, SGS) ---
# Série mensal do dólar (R$/US$, venda, média do mês). Verificada numericamente em 2026-10-09:
# coincide com a média mensal da série diária SGS 1 (dólar comercial venda). Não é a PTAX;
# a página de metadados do BCB não pôde ser consultada.
SGS_CAMBIO = 3698

# --- Clima: pontos de referência em regiões cafeeiras (latitude, longitude) ---
# Coordenadas aproximadas dos municípios; documente e justifique no relatório.
PONTOS_CLIMA = {
    "Sul de Minas (Varginha)": (-21.55, -45.43),
    "Cerrado Mineiro (Patrocinio)": (-18.94, -46.99),
    "Mogiana (Franca)": (-20.54, -47.40),
    "Espirito Santo (Linhares)": (-19.39, -40.07),
}


# # SIDRA/IBGE — IPCA: variação mensal do café moído (%)
# SIDRA_IPCA_CAFE_MOIDO_HISTORICO_URL = (
#     "https://apisidra.ibge.gov.br/values/"
#     "t/1419/n1/1/v/63/p/201501-201912/c315/7392"
# )
#
# SIDRA_IPCA_CAFE_MOIDO_RECENTE_URL = (
#     "https://apisidra.ibge.gov.br/values/"
#     "t/7060/n1/1/v/63/p/202001-202609/c315/7392"
# )