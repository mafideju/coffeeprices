# Modelo de dados

Sem classes: as entidades são arquivos e tabelas.

## Entradas

**`dados/processados/dataset_mensal.csv`** (Fase A, somente leitura): 129 linhas × 49 colunas, 2016-01 a 2026-09.

## Variáveis do modelo (`FEATURES_MODELO`, 13)

| Variável | Hipótese |
|---|---|
| `cambio_medio_var6m`, `cambio_medio_var12m` | H3 |
| `arabica_usd_kg_var6m`, `arabica_usd_kg_var12m` | H3 |
| `chuva_anom_l3`, `chuva_anom_l6` | H6 |
| `tempmin_anom_l3`, `tempmin_anom_l6` | H6 |
| `oni_l6`, `oni_l12` | H7 |
| `mes_sen`, `mes_cos` | H2 |
| `acum12_passado` | H4 |

Regra: nenhuma outra coluna entra nos modelos (inclui `oni` sem defasagem, colunas brutas, `periodo` e os alvos).

## Partição temporal

| Parte | Período | Linhas com alvo | Uso |
|---|---|---|---|
| Treino | 2016-01 a 2021-12 | 72 | ajuste e validação cruzada |
| Intervalo de segurança | 2022-01 a 2022-12 | descartado | evita que o alvo do treino invada o teste |
| Teste | 2023-01 a 2025-09 | 33 | avaliação final, uma única vez |

Validações: tamanhos 72 e 33; sem NaN nas 13 variáveis; último mês de treino + 12 meses < primeiro mês de teste.

## Arquivos intermediários (`dados/processados/`, fora do Git)

- `modelagem_treino.csv`, `modelagem_teste.csv`: colunas `mes`, as 13 variáveis, `alvo_alta`, `alvo_acum_12m`.
- `modelos_treinados.joblib`: pipelines finais (logística, Ridge, RF classificação e RF regressão), ajustados nas 72 linhas de treino.

## Tabelas de saída (`relatorio/tabelas/`)

| Arquivo | Conteúdo | Colunas principais |
|---|---|---|
| `validacao_cruzada.csv` | Nota agrupada de cada configuração testada | tarefa, modelo, hiperparâmetros, nota (macro-F1 ou RMSE), escolhida |
| `hiperparametros_escolhidos.csv` | Configuração final de cada modelo | tarefa, modelo, hiperparâmetros |
| `metricas_classificacao.csv` | Teste, 4 modelos | modelo, macro-F1, acurácia balanceada, VN, FP, FN, VP, n_teste |
| `metricas_regressao.csv` | Teste, 4 modelos | modelo, RMSE, MAE, n_teste |
| `importancia_variaveis.csv` | Importâncias | tarefa, modelo, variável, valor (coeficiente padronizado ou importância) |
| `previsoes_teste.csv` | Previsões linha a linha | mes, alvo real (classe e %), previsão de cada modelo |

Os 4 modelos de cada tarefa: baseline 1, baseline 2, linear, Random Forest. Classificação: logística e Random Forest com `class_weight="balanced"`. Regressão: Ridge e Random Forest sem peso. `hiperparametros_escolhidos.csv` registra também `class_weight` (`balanced` ou vazio).

## Figuras de saída (`relatorio/figuras/`)

`09_comparacao_modelos.png`, `10_matrizes_confusao.png`, `11_previsto_vs_real.png` e `12_importancia_variaveis.png`. Todas trazem a nota "resultados indicativos: teste com 33 linhas".

## Novos itens em `src/config.py`

`FEATURES_MODELO`, `SEMENTE = 42`, `N_SPLITS_CV = 3`, `TAMANHO_VALIDACAO_CV = 12`, `TAMANHOS_ESPERADOS = (72, 33)`, as grades de hiperparâmetros (ordenadas do mais simples ao mais complexo), `TOLERANCIA_MACRO_F1 = 0.03` e `TOLERANCIA_RMSE = 0.03`. Reaproveitam `GAP_MESES` e `ANO_FIM_TREINO`.
