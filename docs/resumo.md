# Resumo das etapas da Fase A (execução e depuração do pipeline)

Data da execução: 2026-10-09. Ambiente: Windows, PowerShell, Python 3.12.2, `.venv`.

## Passo 0: leitura do projeto
- Problema: prever a variação acumulada do IPCA do café moído nos 12 meses seguintes (classificação como foco, regressão complementar).
- Maior risco: coletas 01 a 05, nunca executadas contra as fontes reais.
- `config.py` não centraliza todos os endereços: BCB (montado em `02`), NASA POWER (`03`) e NOAA (`04`) ficam nos scripts; a Pink Sheet é baixada manualmente. Decisão: seguir com os valores existentes.

## Passo 1: constituição
- Gravada em `.specify/memory/constitution.md`, versão 1.0.0, ratificada em 2026-10-09.
- Princípios: dados reais, sem vazamento temporal, validação temporal com baseline obrigatório, simplicidade e configuração central, SDD com mudanças controladas.
- Incluída a orientação de inspecionar o formato real das respostas (JSON ou XML).
- Commit: `docs: establish project constitution v1.0.0`.

## Script 01: IPCA do café moído (SIDRA)
- Rodou. 141 meses, 2015-01 a 2026-09, sem lacunas, ausentes ou duplicatas.
- Filtro correto: "1114022.Café moído", "IPCA - Variação mensal", Brasil.
- Conferência com consulta direta no SIDRA: 2015-01 = 0,04; 2019-12 = 0,00; 2020-01 = -0,23; 2026-09 = -1,09 (todos iguais).
- Faixa: -3,72 a 10,77; média 0,86.
- A API respondeu em JSON, não em XML; parser sem alteração.
- Um `TimeoutError` na tabela 7060 na 1ª execução foi lentidão passageira (curl em 0,3 s); a 2ª execução funcionou.

## Script 02: câmbio (BCB, SGS 3698)
- Rodou. 141 meses, 2015-01 a 2026-09, sem lacunas. Faixa R$ 2,63 a 6,10; média 4,52.
- A série 3698 é mensal e coincide, até a 4ª casa, com a média mensal da série diária SGS 1 (dólar comercial venda): 2023-01 = 5,2007; 2023-02 = 5,1717; 2023-03 = 5,2115.
- A API do BCB foi consultada normalmente. Só a página de metadados do BCB não abriu, então a conclusão é uma inferência numérica, não uma confirmação textual.
- Correção: comentário "PTAX venda" em `config.py` e item do README ajustados. Commit: `fix: correct SGS 3698 description and add corrections log`.

## Script 03: clima (NASA POWER)
- Rodou. 4 pontos × 140 meses (2015-01 a 2026-08), sem nulos e sem -999.
- Chuva média cerca de 3 mm/dia; temperatura mínima entre cerca de 3 e 19 °C.
- Setembro/2026 vem como -999 na API (sem dado) e é descartado: o clima termina em 2026-08.
- Sem alteração de código. Commit: `docs: log NASA POWER missing latest month`.

## Script 04: ONI (NOAA)
- Rodou. 140 meses, 2015-01 a 2026-08, sem lacunas. Faixa -1,11 a 2,59; média 0,22.
- URL ativa e formato `SEAS YR TOTAL ANOM` confirmados. JAS/2026 = 2,16 aparece em 2026-08.
- Setembro/2026 sem valor. Sem alteração de código.

## Script 05: arábica (Banco Mundial)
- Rodou. Planilha atualizada em 02/10/2026, aba "Monthly Prices", coluna 12 "Coffee, Arabica" em $/kg.
- 141 meses, 2015-01 a 2026-09, sem lacunas. Faixa US$ 2,66 a 9,05; média 4,59. Último valor (2026-09) = 7,26.
- Sem alteração de código.

## Script 06: dataset
- 129 linhas × 43 colunas (49 após a Fase A.2), 2016-01 a 2026-09, sem meses duplicados.
- 117 linhas com alvo; 12 últimas (2025-10 a 2026-09) sem alvo, como esperado.
- Classes: 70 de alta, 47 de não alta. Treino: 84 linhas (56% de alta). Teste: 45 linhas, 33 com alvo (70% de alta).
- Alvo conferido manualmente: 2016-01 = 19,8515%; 2022-06 = -4,5572% (iguais ao dataset).
- Sem safra CONAB (arquivo inexistente).
- Atenção: a coluna `oni` (sem defasagem) permanece no dataset. Não deve entrar no modelo. Decisão pendente.

## Script 07: EDA
- 5 tabelas em `relatorio/tabelas/` e 8 figuras em `relatorio/figuras/`.
- `02_acumulada_12m` mostra ciclos: picos de cerca de 67% (2022) e 82% (2025) e vales de cerca de -9% (2018/19 e 2023/24); 2026 chega a -18%.
- `08_alvo_e_divisao_treino_teste` mostra o mesmo desenho, com a linha de início do teste em 2023. O treino contém o ciclo de 2021/22; o teste contém o ciclo de 2024/25 e a queda de 2025/26.

## Fase A.2: ajustes aprovados pelo autor (commit 82d277e)
- `config.py`: `GAP_MESES = 12` e `FEATURES_CANDIDATAS` (36 variáveis; sem `oni` sem defasagem, `chuva_mm_dia` e `temp_min_c` brutos).
- `06`: 6 colunas novas (variação % de 3, 6 e 12 meses de câmbio e arábica). Dataset: 129 × 49. Conferência manual: câmbio, 6 meses, 2020-06 = 26,4503%.
- `07`: `correlacao_com_alvo_treino.csv` (72 linhas, 2016-01 a 2021-12, corte derivado do config).
- Achado: no treino, `cambio_medio_l6` = 0,87 (antes 0,37), `variacao_mensal_l12` = -0,06 (antes -0,44) e `acum12_passado` = +0,31 (antes -0,18). Correlações instáveis (cerca de 6 janelas independentes), só descritivas.
- Avaliação do outro chat: pipeline válido. Decisões ainda abertas: safra CONAB, métricas/baselines (macro-F1 e acurácia balanceada) e gap/validação (Fase B).

## Pendências
- Tratamento da coluna `oni` sem defasagem.
- Safra CONAB (H1 e H5).
- Commit de `relatorio/` (`chore:`), se desejado.
- Decisões metodológicas ficam com o outro chat. A Fase B não foi iniciada.


## Fase B (modelagem), 2026-10-09
- `config.py`: `FEATURES_MODELO` (13), `SEMENTE = 42`, grades, tolerâncias (0,03) e `TAMANHOS_ESPERADOS = (72, 33)`.
- `08`: treino 72 linhas (2016-01 a 2021-12), 2022 descartado, teste 33 linhas (2023-01 a 2025-09), 0 NaN.
- `09`: baselines, logística (`C = 1`), Ridge (`alpha = 100`), RF de classificação (`max_depth = 2`, `min_samples_leaf = 5`) e RF de regressão (`max_depth = 2`, `min_samples_leaf = 10`); `class_weight="balanced"` nos classificadores; validação cruzada temporal com nota agrupada. Ridge: grade ampliada com `alpha = 1000`, sem mudar a escolha.
- `10`: teste aberto uma vez. Classificação: macro-F1 0,4107 (maioria), 0,2993 (persistência), 0,4995 (logística), 0,5227 (RF). Regressão: RMSE 35,0413 (média), 55,8725 (persistência), 37,9301 (Ridge), 38,4511 (RF). Regressão não supera a média. Resultados indicativos.
- `11`: previsão ilustrativa só para 2026-09 (janela 2026-10 a 2027-09); 2026-10 a 2026-12 não é possível sem inventar dados.
- Reprodutibilidade: 2 rodadas completas com hash idêntico nas 12 tabelas.
- Detalhes completos em `docs/pacote-de-retorno-faseb.md`.
