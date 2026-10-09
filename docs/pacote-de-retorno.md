# Pacote de retorno da Fase A

Gerado em 2026-10-09 para colar no outro chat (metodologia e relatório).

## 1. Saída do script 06
```
Aviso: dados/brutos/safra_conab.csv não existe; seguindo sem as variáveis de safra.
Dataset: 129 linhas x 43 colunas, 2016-01 a 2026-09
Linhas com alvo disponível: 117
Distribuição do alvo de classificação (1 = alta):
alvo_alta
1.0    70
0.0    47
Salvo em ...\dados\processados\dataset_mensal.csv
```
Verificação manual do alvo: 2016-01 = 19,8515% (manual) e 19,8515% (dataset); 2022-06 = -4,5572% nos dois.

## 2. Saída do script 07
```
Registros: 129 | Variáveis: 43 | Período: 2016-01 a 2026-09
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

**valores_ausentes.csv:** todas as colunas têm 0 ausentes, exceto: chuva_mm_dia, temp_min_c, oni, chuva_anom, tempmin_anom, chuva_anom_l0, tempmin_anom_l0 (1 cada, 0,8%, referentes a 2026-09) e alvo_acum_12m e alvo_alta (12 cada, 9,3%).

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
- Os últimos meses de 2026 têm quedas seguidas no IPCA do café (-3,72, -2,45, -1,86, -1,09), consistentes com o acumulado negativo.

## 6. Intervalos reais de datas e contagens

| Fonte | Período | Meses |
|---|---|---|
| IPCA café moído (SIDRA 1419 e 7060) | 2015-01 a 2026-09 | 141 |
| Câmbio (SGS 3698) | 2015-01 a 2026-09 | 141 |
| Arábica (Pink Sheet, atualizada em 02/10/2026) | 2015-01 a 2026-09 | 141 |
| Clima (NASA POWER, 4 pontos) | 2015-01 a 2026-08 | 140 por ponto |
| ONI (NOAA) | 2015-01 a 2026-08 | 140 |
| **Dataset final** | **2016-01 a 2026-09** | **129 linhas × 43 colunas** |

- Linhas com alvo: 117 (84 de treino e 33 de teste). O alvo vai até 2025-09.
- Classes: 70 de alta (59,8%) e 47 de não alta (40,2%).
- Por período: treino 47 de alta e 37 de não alta (56%); teste 23 de alta e 10 de não alta (70%).

## 7. Versões
Python 3.12.2, pandas 3.0.6, numpy 2.5.3, requests 2.34.2, matplotlib 3.11.2, openpyxl 3.1.5. scikit-learn não instalado (só na Fase B).

## 8. Decisões que podem afetar a metodologia
Nenhuma foi aplicada. Pontos a decidir no outro chat:
1. Tratamento da coluna `oni` (sem defasagem).
2. Clima e ONI ausentes em 2026-09, que só afetam linhas sem alvo.
3. Teste pequeno e com mudança de proporção de classes, o que torna o baseline "sempre alta" forte no teste.
4. Safra CONAB não disponível (H1 e H5).

## 9. Dúvidas pendentes
- Qual tratamento dar ao `oni`?
- Haverá preenchimento manual da safra CONAB?
- Faço o commit `chore:` de `relatorio/`?
