# Pacote de retorno da Fase A

Gerado em 2026-10-09 para colar no outro chat (metodologia e relatório).

## 1. Saída do script 06
```
Aviso: dados/brutos/safra_conab.csv não existe; seguindo sem as variáveis de safra.
Dataset: 129 linhas x 49 colunas, 2016-01 a 2026-09
Linhas com alvo disponível: 117
Distribuição do alvo de classificação (1 = alta):
alvo_alta
1.0    70
0.0    47
Salvo em ...\dados\processados\dataset_mensal.csv
```
Fase A.2 (commit 82d277e) acrescentou 6 colunas (variações percentuais de 3, 6 e 12 meses de câmbio e arábica). Conferência manual: cambio_medio_var6m em 2020-06 = 26,4503% (manual) e 26,4503% (dataset).

Verificação manual do alvo: 2016-01 = 19,8515% (manual) e 19,8515% (dataset); 2022-06 = -4,5572% nos dois.

## 2. Saída do script 07
```
Registros: 129 | Variáveis: 49 | Período: 2016-01 a 2026-09
Meses duplicados: 0
Ausentes nas variáveis-base:
                 ausentes  percentual
variacao_mensal         0         0.0
acum12_passado          0         0.0
cambio_medio            0         0.0
arabica_usd_kg          0         0.0
chuva_anom              1         0.8
tempmin_anom            1         0.8
oni                     1         0.8
alvo_acum_12m          12         9.3
Outliers (IQR e Z>3):
       variavel  outliers_iqr  outliers_z3
variacao_mensal             7            3
 acum12_passado             7            0
   cambio_medio             0            0
 arabica_usd_kg             0            0
     chuva_anom            14            1
   tempmin_anom             1            1
            oni             1            0
  alvo_acum_12m             5            0
Classes do alvo (1=alta): {1.0: 70, 0.0: 47}
Maiores correlações com o alvo (janelas de 12 meses se sobrepõem e inflam a correlação):
variacao_mensal_l12   -0.44
cambio_medio_l0        0.42
cambio_medio_l3        0.39
cambio_medio_l6        0.37
variacao_mensal_l0     0.35
oni_l6                 0.33
cambio_medio_l12       0.31
tempmin_anom_l6        0.28
Gráficos: 01_variacao_mensal, 02_acumulada_12m, 03_histograma_variacao, 04_boxplot_sazonalidade,
05_variaveis_explicativas, 06_matriz_correlacao, 07_correlacao_lags_alvo, 08_alvo_e_divisao_treino_teste (.png)
```

## 3. Tabelas de `relatorio/tabelas/`

**estatisticas_descritivas.csv**

| variável | n | média | dp | mín | 25% | 50% | 75% | máx |
|---|---|---|---|---|---|---|---|---|
| variacao_mensal | 129 | 0,854 | 2,435 | -3,72 | -0,69 | 0,17 | 1,68 | 10,77 |
| acum12_passado | 129 | 14,50 | 24,75 | -17,80 | -6,77 | 7,96 | 22,65 | 82,25 |
| cambio_medio | 129 | 4,635 | 0,889 | 3,1042 | 3,7867 | 4,9837 | 5,3409 | 6,097 |
| arabica_usd_kg | 129 | 4,688 | 1,820 | 2,66 | 3,24 | 4,05 | 5,76 | 9,05 |
| chuva_anom | 128 | -0,114 | 1,375 | -5,148 | -0,710 | -0,151 | 0,500 | 3,857 |
| tempmin_anom | 128 | 0,088 | 1,424 | -4,530 | -0,647 | 0,067 | 1,089 | 3,114 |
| oni | 128 | 0,098 | 0,812 | -1,11 | -0,55 | -0,075 | 0,575 | 2,50 |
| alvo_acum_12m | 117 | 14,20 | 25,96 | -17,80 | -7,32 | 5,65 | 23,47 | 82,25 |

**valores_ausentes.csv** (49 colunas; as 6 novas têm 0 ausentes): todas as colunas têm 0 ausentes, exceto: chuva_mm_dia, temp_min_c, oni, chuva_anom, tempmin_anom, chuva_anom_l0, tempmin_anom_l0 (1 cada, 0,8%, referentes a 2026-09) e alvo_acum_12m e alvo_alta (12 cada, 9,3%).

**outliers.csv:** igual à tabela impressa pelo script 07.

**matriz_correlacao.csv** (variáveis-base, 2 casas)

| | var_mensal | acum12 | câmbio | arábica | chuva_anom | tmin_anom | oni | alvo |
|---|---|---|---|---|---|---|---|---|
| variacao_mensal | 1,00 | 0,54 | 0,31 | 0,27 | -0,10 | 0,07 | -0,29 | 0,35 |
| acum12_passado | 0,54 | 1,00 | 0,34 | 0,61 | -0,04 | -0,20 | -0,52 | -0,18 |
| cambio_medio | 0,31 | 0,34 | 1,00 | 0,66 | -0,09 | 0,13 | -0,21 | 0,42 |
| arabica_usd_kg | 0,27 | 0,61 | 0,66 | 1,00 | -0,14 | 0,03 | -0,17 | 0,06 |
| chuva_anom | -0,10 | -0,04 | -0,09 | -0,14 | 1,00 | -0,04 | 0,03 | -0,22 |
| tempmin_anom | 0,07 | -0,20 | 0,13 | 0,03 | -0,04 | 1,00 | 0,28 | 0,26 |
| oni | -0,29 | -0,52 | -0,21 | -0,17 | 0,03 | 0,28 | 1,00 | 0,07 |
| alvo_acum_12m | 0,35 | -0,18 | 0,42 | 0,06 | -0,22 | 0,26 | 0,07 | 1,00 |

**correlacao_com_alvo.csv** (27 linhas, ordenadas por |r|): variacao_mensal_l12 -0,437; cambio_medio_l0 0,420; cambio_medio_l3 0,388; cambio_medio_l6 0,370; variacao_mensal_l0 0,354; oni_l6 0,329; cambio_medio_l12 0,311; tempmin_anom_l6 0,278; chuva_anom_l3 -0,265; tempmin_anom_l0 0,264; tempmin_anom_l3 0,257; variacao_mensal_l6 -0,241; variacao_mensal_l1 0,230; chuva_anom_l0 -0,215; chuva_anom_l6 -0,200; oni_l12 0,194; tempmin_anom_l9 0,192; oni_l2 0,188; acum12_passado -0,183; arabica_usd_kg_l6 -0,154; chuva_anom_l9 -0,117; arabica_usd_kg_l3 -0,086; tempmin_anom_l12 0,074; arabica_usd_kg_l0 0,065; arabica_usd_kg_l12 -0,046; chuva_anom_l12 0,025; variacao_mensal_l3 -0,012.

## 4. Correções feitas (`docs/registro-de-correcoes.md`)

| Data | Script | Erro | Causa | Correção |
|---|---|---|---|---|
| 2026-10-09 | 01 | `TimeoutError` na tabela 7060 (120 s) | Lentidão passageira do servidor SIDRA; `curl` respondeu em 0,3 s | Nenhuma; reexecução funcionou |
| 2026-10-09 | config.py / README (02) | Comentário dizia "PTAX venda" sem evidência | A série 3698 coincide com a média mensal do dólar comercial venda (SGS 1) | Comentário e README corrigidos |
| 2026-10-09 | 03 | Sem erro; clima termina em 2026-08 | NASA POWER devolve -999 para 2026-09 | Nenhuma; limitação registrada |

Nenhum código de coleta precisou ser alterado. As APIs responderam em JSON (não em XML).

## 5. Problemas de qualidade dos dados
- Setembro/2026 sem clima e sem ONI (as fontes não publicaram). A linha tem alvo vazio de qualquer forma.
- 12 meses sem alvo (2025-10 a 2026-09), como esperado.
- A coluna `oni` (sem defasagem) permanece no dataset ao lado de `oni_l2/l6/l12`. Ela viola a regra do ONI e não deve entrar no modelo. Decisão pendente: removê-la do dataset ou excluí-la na seleção de variáveis.
- A página de metadados do BCB não abriu: a série 3698 foi verificada só por comparação numérica com a SGS 1.
- Safra CONAB inexistente: H1 e H5 ficam sem variáveis.
- A proporção de alta muda entre treino e teste (56% para 70%), e o teste tem só 33 linhas com alvo, com janelas sobrepostas.
- Muitos outliers IQR em chuva_anom (14) e variacao_mensal (7); o Z-score aponta 1 e 3.
- As correlações com o alvo calculadas com todas as linhas incluem o teste; para escolher variáveis vale só a tabela do treino (seção 10).
- Os últimos meses de 2026 têm quedas seguidas no IPCA do café (-3,72, -2,45, -1,86, -1,09), consistentes com o acumulado negativo.

## 6. Intervalos reais de datas e contagens

| Fonte | Período | Meses |
|---|---|---|
| IPCA café moído (SIDRA 1419 e 7060) | 2015-01 a 2026-09 | 141 |
| Câmbio (SGS 3698) | 2015-01 a 2026-09 | 141 |
| Arábica (Pink Sheet, atualizada em 02/10/2026) | 2015-01 a 2026-09 | 141 |
| Clima (NASA POWER, 4 pontos) | 2015-01 a 2026-08 | 140 por ponto |
| ONI (NOAA) | 2015-01 a 2026-08 | 140 |
| **Dataset final** | **2016-01 a 2026-09** | **129 linhas × 49 colunas** |

- Linhas com alvo: 117 (84 de treino e 33 de teste). O alvo vai até 2025-09.
- Classes: 70 de alta (59,8%) e 47 de não alta (40,2%).
- Por período: treino 47 de alta e 37 de não alta (56%); teste 23 de alta e 10 de não alta (70%).

## 7. Versões
Python 3.12.2, pandas 3.0.6, numpy 2.5.3, requests 2.34.2, matplotlib 3.11.2, openpyxl 3.1.5. scikit-learn não instalado (só na Fase B).

## 8. Decisões que podem afetar a metodologia
Aplicada com aprovação do autor (Fase A.2): criação das variações percentuais de câmbio e arábica, da lista FEATURES_CANDIDATAS e de GAP_MESES = 12 no config. Pontos ainda a decidir no outro chat:
1. Coluna `oni` sem defasagem: fora de FEATURES_CANDIDATAS, mantida no arquivo.
2. Clima e ONI ausentes em 2026-09, que só afetam linhas sem alvo.
3. Teste pequeno e com mudança de proporção de classes, o que torna o baseline "sempre alta" forte no teste.
4. Safra CONAB não disponível (H1 e H5).

## 9. Dúvidas pendentes
- Haverá preenchimento manual da safra CONAB?
- Safra CONAB, métricas e baselines, e gap/validação (esta só na Fase B): decisões em aberto.


## 10. FEATURES_CANDIDATAS (36 variáveis, `src/config.py`)
Fora da lista: `oni` sem defasagem, `chuva_mm_dia` e `temp_min_c` brutos, `mes_do_ano`, colunas originais sem sufixo (duplicam as `_l0`), alvos, `periodo`, `mes`.

1. mes_sen, mes_cos
2. acum3_passado, acum12_passado
3. variacao_mensal_l0, _l1, _l3, _l6, _l12
4. cambio_medio_l0, _l3, _l6, _l12
5. arabica_usd_kg_l0, _l3, _l6, _l12
6. cambio_medio_var3m, _var6m, _var12m
7. arabica_usd_kg_var3m, _var6m, _var12m
8. chuva_anom_l0, _l3, _l6, _l9, _l12
9. tempmin_anom_l0, _l3, _l6, _l9, _l12
10. oni_l2, oni_l6, oni_l12

## 11. Dicionário de dados do dataset (49 colunas, 129 linhas)

| Variável | dtype | Não nulos | Unidade / descrição |
|---|---|---|---|
| mes | datetime64 | 129 | Primeiro dia do mês |
| variacao_mensal | float64 | 129 | IPCA café moído, variação mensal (%) |
| cambio_medio | float64 | 129 | Dólar venda, média do mês (R$/US$), SGS 3698 |
| chuva_mm_dia | float64 | 128 | Chuva média dos 4 pontos (mm/dia), NASA POWER (bruta, fora da lista) |
| temp_min_c | float64 | 128 | Temperatura mínima média dos 4 pontos (°C) (bruta, fora da lista) |
| oni | float64 | 128 | ONI sem defasagem (índice, °C); NÃO usar no modelo |
| arabica_usd_kg | float64 | 129 | Arábica, Banco Mundial (US$/kg) |
| mes_do_ano | int64 | 129 | Mês (1 a 12); fora da lista (usa-se seno e cosseno) |
| mes_sen, mes_cos | float64 | 129 | Sazonalidade: seno e cosseno de 2π·mês/12 |
| chuva_anom | float64 | 128 | Chuva menos a média do mesmo mês no treino (mm/dia) |
| tempmin_anom | float64 | 128 | Temperatura mínima menos a média do mesmo mês no treino (°C) |
| acum3_passado | float64 | 129 | IPCA do café acumulado nos 3 meses até t (%) |
| acum12_passado | float64 | 129 | IPCA do café acumulado nos 12 meses até t (%) |
| alvo_acum_12m | float64 | 117 | ALVO regressão: variação acumulada de t+1 a t+12 (%) |
| alvo_alta | float64 | 117 | ALVO classificação: 1 se alvo_acum_12m > 0, senão 0 |
| variacao_mensal_l0, _l1, _l3, _l6, _l12 | float64 | 129 cada | variacao_mensal defasada em 0, 1, 3, 6 e 12 meses (%) |
| cambio_medio_l0, _l3, _l6, _l12 | float64 | 129 cada | Câmbio defasado (R$/US$) |
| arabica_usd_kg_l0, _l3, _l6, _l12 | float64 | 129 cada | Arábica defasado (US$/kg) |
| chuva_anom_l0 | float64 | 128 | Anomalia de chuva, defasagem 0 (mm/dia) |
| chuva_anom_l3, _l6, _l9, _l12 | float64 | 129 cada | Anomalia de chuva defasada (mm/dia) |
| tempmin_anom_l0 | float64 | 128 | Anomalia de temp. mínima, defasagem 0 (°C) |
| tempmin_anom_l3, _l6, _l9, _l12 | float64 | 129 cada | Anomalia de temp. mínima defasada (°C) |
| oni_l2, oni_l6, oni_l12 | float64 | 129 cada | ONI defasado em 2, 6 e 12 meses (índice) |
| cambio_medio_var3m, _var6m, _var12m | float64 | 129 cada | NOVAS: variação % do câmbio em 3, 6 e 12 meses |
| arabica_usd_kg_var3m, _var6m, _var12m | float64 | 129 cada | NOVAS: variação % do arábica em 3, 6 e 12 meses |
| periodo | str | 129 | "treino" (até 2022) ou "teste" |

## 12. correlacao_com_alvo_treino.csv (completa)
Só 72 linhas (2016-01 a 2021-12, com alvo disponível e gap de 12 meses); alvo = `alvo_acum_12m`. Linhas em **negrito** são as variações novas (var3m/var6m/var12m) de câmbio e arábica. São correlações descritivas, com janelas sobrepostas (cerca de 6 janelas independentes).

| # | Variável | r |
|---|---|---|
| 1 | cambio_medio_l6 | 0,874 |
| 2 | cambio_medio_l3 | 0,826 |
| 3 | cambio_medio_l12 | 0,719 |
| 4 | cambio_medio_l0 | 0,713 |
| 5 | **arabica_usd_kg_var12m** | **0,556** |
| 6 | **arabica_usd_kg_var6m** | **0,552** |
| 7 | arabica_usd_kg_l0 | 0,547 |
| 8 | **arabica_usd_kg_var3m** | **0,504** |
| 9 | variacao_mensal_l0 | 0,453 |
| 10 | acum3_passado | 0,435 |
| 11 | arabica_usd_kg_l3 | 0,421 |
| 12 | variacao_mensal_l1 | 0,409 |
| 13 | acum12_passado | 0,305 |
| 14 | variacao_mensal_l3 | 0,292 |
| 15 | oni_l2 | -0,291 |
| 16 | chuva_anom_l3 | -0,286 |
| 17 | arabica_usd_kg_l6 | 0,262 |
| 18 | chuva_anom_l0 | -0,226 |
| 19 | chuva_anom_l6 | -0,217 |
| 20 | variacao_mensal_l6 | 0,196 |
| 21 | **cambio_medio_var3m** | **-0,188** |
| 22 | tempmin_anom_l6 | 0,180 |
| 23 | **cambio_medio_var6m** | **-0,177** |
| 24 | tempmin_anom_l9 | 0,164 |
| 25 | oni_l6 | -0,152 |
| 26 | **cambio_medio_var12m** | **0,134** |
| 27 | tempmin_anom_l12 | 0,094 |
| 28 | tempmin_anom_l3 | 0,094 |
| 29 | chuva_anom_l12 | 0,072 |
| 30 | oni_l12 | 0,067 |
| 31 | variacao_mensal_l12 | -0,063 |
| 32 | chuva_anom_l9 | -0,057 |
| 33 | arabica_usd_kg_l12 | -0,047 |
| 34 | mes_sen | 0,040 |
| 35 | tempmin_anom_l0 | -0,037 |
| 36 | mes_cos | -0,034 |

Comparação com a tabela de todas as linhas (seção 3): `cambio_medio_l6` passa de 0,37 para 0,87; `variacao_mensal_l12` de -0,44 para -0,06; `acum12_passado` de -0,18 para +0,31; `tempmin_anom_l6` de 0,28 para 0,18. As variações novas de câmbio têm correlação baixa (-0,19 a 0,13); as de arábica ficam entre 0,50 e 0,56.

## 13. Fase B (modelagem)

A Fase B está concluída (scripts 08, 09, 10 e 11). O pacote completo, com as saídas dos scripts, as tabelas de métricas e de importância, os hiperparâmetros, as figuras, as versões e as dúvidas, está em `docs/pacote-de-retorno-faseb.md`.
