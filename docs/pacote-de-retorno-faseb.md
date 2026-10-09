# Pacote de retorno da Fase B (modelagem)

Gerado em 2026-10-09 para o outro chat (metodologia e relatório). Todos os números abaixo foram copiados das saídas reais dos scripts e das tabelas em `relatorio/tabelas/`. Nada foi resumido ou inventado. Os resultados do teste (33 linhas, cerca de 3 janelas independentes) são **indicativos**.

## 1. Resumo da Fase B

- Variáveis (13, fixas pelas hipóteses H2, H3, H4, H6 e H7): `cambio_medio_var6m`, `cambio_medio_var12m`, `arabica_usd_kg_var6m`, `arabica_usd_kg_var12m`, `chuva_anom_l3`, `chuva_anom_l6`, `tempmin_anom_l3`, `tempmin_anom_l6`, `oni_l6`, `oni_l12`, `mes_sen`, `mes_cos`, `acum12_passado`.
- Divisão: treino 2016-01 a 2021-12 (72 linhas), 2022 descartado (intervalo de 12 meses), teste 2023-01 a 2025-09 (33 linhas).
- Modelos: baselines (maioria e persistência do sinal; média e persistência), logística e Ridge (padronização no `Pipeline`), Random Forest (300 árvores, profundidade limitada). `class_weight="balanced"` só nos classificadores. Semente 42.
- Validação cruzada temporal: `TimeSeriesSplit(n_splits=3, test_size=12, gap=12)`, nota única sobre as previsões agrupadas dos 3 folds; desempate pela configuração mais simples dentro de 0,03 (macro-F1 absoluto, RMSE relativo). Ridge: grade ampliada com `alpha = 1000` depois de conferência de borda (só treino); a escolha seguiu `alpha = 100`.
- Resultado no teste: classificação, logística (macro-F1 0,4995) e RF (0,5227) acima do baseline de maioria (0,4107), mas a acurácia balanceada quase não muda (0,5043 e 0,5261 contra 0,5000). Regressão: nenhum modelo supera a média do treino (RMSE 35,0413 contra 37,9301 do Ridge e 38,4511 do RF), então a premissa de aceitação (RMSE ao menos 10% menor) não foi cumprida. Reportado como está.

## 2. Saída completa do script 08 (`src/08_preparar_modelagem.py`)

```text
Treino: 72 linhas (2016-01 a 2021-12)
Descartado (intervalo de segurança): 12 linhas (2022-01 a 2022-12)
Teste: 33 linhas (2023-01 a 2025-09)
Proporção de alta: treino 61% (44 de 72), teste 70% (23 de 33)
Variáveis do modelo (13): cambio_medio_var6m, cambio_medio_var12m, arabica_usd_kg_var6m, arabica_usd_kg_var12m, chuva_anom_l3, chuva_anom_l6, tempmin_anom_l3, tempmin_anom_l6, oni_l6, oni_l12, mes_sen, mes_cos, acum12_passado
NaN nas variáveis: treino 0, teste 0
Último mês coberto pelo alvo do treino: 2022-12 (teste começa em 2023-01)
OK: gravados modelagem_treino.csv e modelagem_teste.csv em dados/processados/
```

## 3. Saída completa do script 09 (`src/09_treinar_modelos.py`)

```text
Treino lido: 72 linhas (2016-01 a 2021-12)
Validação cruzada temporal: TimeSeriesSplit(n_splits=3, test_size=12, gap=12)
  Divisão 1: treino 24 linhas (2016-01 a 2017-12), alta 14 e queda 10 | validação 12 linhas (2019-01 a 2019-12), alta 6 e queda 6
  AVISO: o treino da divisão 1 tem só 24 linhas (menos de 30); resultado instável.
  Divisão 2: treino 36 linhas (2016-01 a 2018-12), alta 14 e queda 22 | validação 12 linhas (2020-01 a 2020-12), alta 12 e queda 0
  Divisão 3: treino 48 linhas (2016-01 a 2019-12), alta 20 e queda 28 | validação 12 linhas (2021-01 a 2021-12), alta 12 e queda 0

Baselines (nota agrupada da validação; classificação = macro-F1, regressão = RMSE):
Verificação de escala (exemplo 2019-01): acum12_passado = -8.26, alvo_acum_12m = -7.37
  acum12_passado: mínimo -9.49, máximo 50.24
  alvo_acum_12m: mínimo -9.49, máximo 67.53
  Mesma unidade (%), razão dos desvios-padrão = 1.64
  classificacao baseline_maioria             0.1429
  classificacao baseline_persistencia_sinal  0.6250
  regressao     baseline_media               32.9699
  regressao     baseline_persistencia        28.7096

logistica (macro-F1, nota agrupada):
  {'C': 0.01}                                   0.6486 
  {'C': 0.1}                                    0.7231 
  {'C': 1}                                      0.7778 <- escolhida
  {'C': 10}                                     0.7498 

ridge (RMSE, nota agrupada):
  {'alpha': 1000}                               32.5815 
  {'alpha': 100}                                31.5008 <- escolhida
  {'alpha': 10}                                 32.5360 
  {'alpha': 1}                                  34.5734 
  {'alpha': 0.1}                                34.9655 

rf_classificacao (macro-F1, nota agrupada):
  {'max_depth': 2, 'min_samples_leaf': 10}      0.3793 
  {'max_depth': 2, 'min_samples_leaf': 5}       0.5982 <- escolhida
  {'max_depth': 3, 'min_samples_leaf': 10}      0.3793 
  {'max_depth': 3, 'min_samples_leaf': 5}       0.6211 
  {'max_depth': 4, 'min_samples_leaf': 10}      0.3793 
  {'max_depth': 4, 'min_samples_leaf': 5}       0.6211 

rf_regressao (RMSE, nota agrupada):
  {'max_depth': 2, 'min_samples_leaf': 10}      34.6335 <- escolhida
  {'max_depth': 2, 'min_samples_leaf': 5}       33.9500 
  {'max_depth': 3, 'min_samples_leaf': 10}      34.6335 
  {'max_depth': 3, 'min_samples_leaf': 5}       33.9723 
  {'max_depth': 4, 'min_samples_leaf': 10}      34.6335 
  {'max_depth': 4, 'min_samples_leaf': 5}       33.9730 

Baselines do treino inteiro: classe majoritária = 1, média do alvo = 12.16
Gravados: validacao_cruzada.csv, hiperparametros_escolhidos.csv e modelos_treinados.joblib
```

## 4. Saída completa do script 10 (`src/10_avaliar_modelos.py`)

```text
Teste: 33 linhas (2023-01 a 2025-09)
AVISO: resultados indicativos: teste com 33 linhas (cerca de 3 janelas independentes)

Classificação (teste):
                     modelo  macro_f1  acuracia_balanceada  VN  FP  FN  VP  n_teste
           baseline_maioria    0.4107               0.5000   0  10   0  23       33
baseline_persistencia_sinal    0.2993               0.2891   1   9  12  11       33
                  logistica    0.4995               0.5043   4   6   9  14       33
           rf_classificacao    0.5227               0.5261   4   6   8  15       33

Regressão (teste):
               modelo    rmse     mae  n_teste
       baseline_media 35.0413 28.9124       33
baseline_persistencia 55.8725 46.7783       33
                ridge 37.9301 32.3103       33
         rf_regressao 38.4511 32.4723       33

Importância das variáveis (coeficientes padronizados da logística e do Ridge; importância do Random Forest), ordenada por |valor|:
  classificacao / logistica:
    arabica_usd_kg_var12m    +1.6972
    arabica_usd_kg_var6m     +1.5640
    oni_l12                  +1.4253
    oni_l6                   +0.9637
    cambio_medio_var12m      +0.6525
    tempmin_anom_l6          +0.5157
    mes_sen                  -0.3248
    chuva_anom_l6            -0.3148
    chuva_anom_l3            -0.2927
    acum12_passado           +0.1967
    mes_cos                  +0.1867
    cambio_medio_var6m       +0.1727
    tempmin_anom_l3          +0.1097
  regressao / ridge:
    arabica_usd_kg_var12m    +3.6136
    arabica_usd_kg_var6m     +3.5764
    chuva_anom_l3            -2.4487
    cambio_medio_var12m      +2.2796
    cambio_medio_var6m       -1.7466
    tempmin_anom_l6          +1.6801
    oni_l6                   -1.5567
    chuva_anom_l6            -1.5201
    acum12_passado           +1.2113
    oni_l12                  +0.8433
    tempmin_anom_l3          +0.8405
    mes_cos                  -0.7336
    mes_sen                  +0.7236
  classificacao / rf_classificacao:
    arabica_usd_kg_var12m    +0.2799
    arabica_usd_kg_var6m     +0.2556
    oni_l12                  +0.1395
    oni_l6                   +0.0763
    tempmin_anom_l6          +0.0495
    acum12_passado           +0.0414
    tempmin_anom_l3          +0.0410
    cambio_medio_var12m      +0.0399
    cambio_medio_var6m       +0.0330
    chuva_anom_l3            +0.0212
    chuva_anom_l6            +0.0097
    mes_sen                  +0.0067
    mes_cos                  +0.0064
  regressao / rf_regressao:
    arabica_usd_kg_var12m    +0.5680
    oni_l12                  +0.1514
    arabica_usd_kg_var6m     +0.1252
    oni_l6                   +0.1149
    acum12_passado           +0.0201
    chuva_anom_l6            +0.0071
    tempmin_anom_l6          +0.0057
    chuva_anom_l3            +0.0055
    cambio_medio_var6m       +0.0021
    mes_sen                  +0.0000
    cambio_medio_var12m      +0.0000
    tempmin_anom_l3          +0.0000
    mes_cos                  +0.0000

Figuras gravadas em C:\Projetos\Python\TCC\cafe-ml\cafe-ml\relatorio\figuras: 09_comparacao_modelos.png, 10_matrizes_confusao.png, 11_previsto_vs_real.png, 12_importancia_variaveis.png
```

## 5. Tabelas

### 5.1 Métricas de classificação no teste (`metricas_classificacao.csv`)

| modelo | macro_f1 | acuracia_balanceada | VN | FP | FN | VP | n_teste |
|---|---|---|---|---|---|---|---|
| baseline_maioria | 0,4107 | 0,5000 | 0 | 10 | 0 | 23 | 33 |
| baseline_persistencia_sinal | 0,2993 | 0,2891 | 1 | 9 | 12 | 11 | 33 |
| logistica | 0,4995 | 0,5043 | 4 | 6 | 9 | 14 | 33 |
| rf_classificacao | 0,5227 | 0,5261 | 4 | 6 | 8 | 15 | 33 |

### 5.2 Métricas de regressão no teste (`metricas_regressao.csv`)

| modelo | rmse | mae | n_teste |
|---|---|---|---|
| baseline_media | 35,0413 | 28,9124 | 33 |
| baseline_persistencia | 55,8725 | 46,7783 | 33 |
| ridge | 37,9301 | 32,3103 | 33 |
| rf_regressao | 38,4511 | 32,4723 | 33 |

### 5.3 Importância das variáveis (`importancia_variaveis.csv`, 52 linhas)

| tarefa | modelo | variavel | valor |
|---|---|---|---|
| classificacao | logistica | cambio_medio_var6m | 0,1727 |
| classificacao | logistica | cambio_medio_var12m | 0,6525 |
| classificacao | logistica | arabica_usd_kg_var6m | 1,5640 |
| classificacao | logistica | arabica_usd_kg_var12m | 1,6972 |
| classificacao | logistica | chuva_anom_l3 | -0,2927 |
| classificacao | logistica | chuva_anom_l6 | -0,3148 |
| classificacao | logistica | tempmin_anom_l3 | 0,1097 |
| classificacao | logistica | tempmin_anom_l6 | 0,5157 |
| classificacao | logistica | oni_l6 | 0,9637 |
| classificacao | logistica | oni_l12 | 1,4253 |
| classificacao | logistica | mes_sen | -0,3248 |
| classificacao | logistica | mes_cos | 0,1867 |
| classificacao | logistica | acum12_passado | 0,1967 |
| regressao | ridge | cambio_medio_var6m | -1,7466 |
| regressao | ridge | cambio_medio_var12m | 2,2796 |
| regressao | ridge | arabica_usd_kg_var6m | 3,5764 |
| regressao | ridge | arabica_usd_kg_var12m | 3,6136 |
| regressao | ridge | chuva_anom_l3 | -2,4487 |
| regressao | ridge | chuva_anom_l6 | -1,5201 |
| regressao | ridge | tempmin_anom_l3 | 0,8405 |
| regressao | ridge | tempmin_anom_l6 | 1,6801 |
| regressao | ridge | oni_l6 | -1,5567 |
| regressao | ridge | oni_l12 | 0,8433 |
| regressao | ridge | mes_sen | 0,7236 |
| regressao | ridge | mes_cos | -0,7336 |
| regressao | ridge | acum12_passado | 1,2113 |
| classificacao | rf_classificacao | cambio_medio_var6m | 0,0330 |
| classificacao | rf_classificacao | cambio_medio_var12m | 0,0399 |
| classificacao | rf_classificacao | arabica_usd_kg_var6m | 0,2556 |
| classificacao | rf_classificacao | arabica_usd_kg_var12m | 0,2799 |
| classificacao | rf_classificacao | chuva_anom_l3 | 0,0212 |
| classificacao | rf_classificacao | chuva_anom_l6 | 0,0097 |
| classificacao | rf_classificacao | tempmin_anom_l3 | 0,0410 |
| classificacao | rf_classificacao | tempmin_anom_l6 | 0,0495 |
| classificacao | rf_classificacao | oni_l6 | 0,0763 |
| classificacao | rf_classificacao | oni_l12 | 0,1395 |
| classificacao | rf_classificacao | mes_sen | 0,0067 |
| classificacao | rf_classificacao | mes_cos | 0,0064 |
| classificacao | rf_classificacao | acum12_passado | 0,0414 |
| regressao | rf_regressao | cambio_medio_var6m | 0,0021 |
| regressao | rf_regressao | cambio_medio_var12m | 0,0000 |
| regressao | rf_regressao | arabica_usd_kg_var6m | 0,1252 |
| regressao | rf_regressao | arabica_usd_kg_var12m | 0,5680 |
| regressao | rf_regressao | chuva_anom_l3 | 0,0055 |
| regressao | rf_regressao | chuva_anom_l6 | 0,0071 |
| regressao | rf_regressao | tempmin_anom_l3 | 0,0000 |
| regressao | rf_regressao | tempmin_anom_l6 | 0,0057 |
| regressao | rf_regressao | oni_l6 | 0,1149 |
| regressao | rf_regressao | oni_l12 | 0,1514 |
| regressao | rf_regressao | mes_sen | 0,0000 |
| regressao | rf_regressao | mes_cos | 0,0000 |
| regressao | rf_regressao | acum12_passado | 0,0201 |

### 5.4 Hiperparâmetros escolhidos (`hiperparametros_escolhidos.csv`)

| tarefa | modelo | hiperparametros | class_weight |
|---|---|---|---|
| classificacao | logistica | {'C': 1} | balanced |
| regressao | ridge | {'alpha': 100} |  |
| classificacao | rf_classificacao | {'max_depth': 2, 'min_samples_leaf': 5} | balanced |
| regressao | rf_regressao | {'max_depth': 2, 'min_samples_leaf': 10} |  |

### 5.5 Validação cruzada (`validacao_cruzada.csv`)

| tarefa | modelo | hiperparametros | nota | escolhida |
|---|---|---|---|---|
| classificacao | baseline_maioria |  | 0,1429 | baseline |
| classificacao | baseline_persistencia_sinal |  | 0,6250 | baseline |
| regressao | baseline_media |  | 32,9699 | baseline |
| regressao | baseline_persistencia |  | 28,7096 | baseline |
| classificacao | logistica | {'C': 0.01} | 0,6486 |  |
| classificacao | logistica | {'C': 0.1} | 0,7231 |  |
| classificacao | logistica | {'C': 1} | 0,7778 | sim |
| classificacao | logistica | {'C': 10} | 0,7498 |  |
| regressao | ridge | {'alpha': 1000} | 32,5815 |  |
| regressao | ridge | {'alpha': 100} | 31,5008 | sim |
| regressao | ridge | {'alpha': 10} | 32,5360 |  |
| regressao | ridge | {'alpha': 1} | 34,5734 |  |
| regressao | ridge | {'alpha': 0.1} | 34,9655 |  |
| classificacao | rf_classificacao | {'max_depth': 2, 'min_samples_leaf': 10} | 0,3793 |  |
| classificacao | rf_classificacao | {'max_depth': 2, 'min_samples_leaf': 5} | 0,5982 | sim |
| classificacao | rf_classificacao | {'max_depth': 3, 'min_samples_leaf': 10} | 0,3793 |  |
| classificacao | rf_classificacao | {'max_depth': 3, 'min_samples_leaf': 5} | 0,6211 |  |
| classificacao | rf_classificacao | {'max_depth': 4, 'min_samples_leaf': 10} | 0,3793 |  |
| classificacao | rf_classificacao | {'max_depth': 4, 'min_samples_leaf': 5} | 0,6211 |  |
| regressao | rf_regressao | {'max_depth': 2, 'min_samples_leaf': 10} | 34,6335 | sim |
| regressao | rf_regressao | {'max_depth': 2, 'min_samples_leaf': 5} | 33,9500 |  |
| regressao | rf_regressao | {'max_depth': 3, 'min_samples_leaf': 10} | 34,6335 |  |
| regressao | rf_regressao | {'max_depth': 3, 'min_samples_leaf': 5} | 33,9723 |  |
| regressao | rf_regressao | {'max_depth': 4, 'min_samples_leaf': 10} | 34,6335 |  |
| regressao | rf_regressao | {'max_depth': 4, 'min_samples_leaf': 5} | 33,9730 |  |

### 5.6 Tamanhos e classes de cada divisão da validação cruzada

| Divisão | Treino | Classes do treino | Validação | Classes da validação |
|---|---|---|---|---|
| 1 | 24 linhas (2016-01 a 2017-12) | 14 alta e 10 queda | 12 linhas (2019) | 6 alta e 6 queda |
| 2 | 36 linhas (2016-01 a 2018-12) | 14 alta e 22 queda | 12 linhas (2020) | 12 alta e 0 queda |
| 3 | 48 linhas (2016-01 a 2019-12) | 20 alta e 28 queda | 12 linhas (2021) | 12 alta e 0 queda |

Aviso do script: o treino da divisão 1 tem só 24 linhas (resultado instável). A nota agrupada se apoia em 6 meses de queda.

### 5.7 Previsão ilustrativa para 2026-09 (T014, aprovada pelo autor)

```text
PREVISÃO ILUSTRATIVA para 2026-09 (janela 2026-10 a 2027-09; não há valor real para comparar).
Os modelos têm desempenho modesto no teste (macro-F1 0,50 e 0,52; regressão sem superar a média).
Classificação: 1 = alta, 0 = queda. Regressão: variação acumulada em %.

       tarefa                      modelo  previsao
classificacao            baseline_maioria      1.00
classificacao baseline_persistencia_sinal      0.00
classificacao                   logistica      0.00
classificacao            rf_classificacao      0.00
    regressao              baseline_media     12.16
    regressao       baseline_persistencia    -17.80
    regressao                       ridge     -1.24
    regressao                rf_regressao     -5.51
```

Arquivo: `relatorio/tabelas/previsao_ilustrativa_2026-09.csv`. **Ilustrativa**: sem valor real para comparar, janela prevista 2026-10 a 2027-09. Previsão para 2026-10, 2026-11 e 2026-12 **não foi feita**: câmbio, arábica e IPCA só existem até 2026-09, e as variáveis `var6m/var12m` e `acum12_passado` desses meses exigiriam valores inventados.

## 6. Figuras geradas (`relatorio/figuras/`)

- `09_comparacao_modelos.png`
- `10_matrizes_confusao.png`
- `11_previsto_vs_real.png`
- `12_importancia_variaveis.png`

Todas com a nota "resultados indicativos: teste com 33 linhas (cerca de 3 janelas independentes)".

## 7. Correções e decisões da Fase B (de `docs/registro-de-correcoes.md`)

| Data | Script | Erro | Causa | Correção |
|---|---|---|---|---|
| 2026-10-09 | 01_coletar_ipca.py | `TimeoutError` na tabela 7060 (120 s) | Lentidão passageira do servidor SIDRA; `curl` respondeu em 0,3 s e a nova execução funcionou | Nenhuma alteração de código |
| 2026-10-09 | config.py / README.md (02) | Comentário dizia "PTAX venda", sem evidência | Série 3698 não é a PTAX: coincide com a média mensal do dólar comercial venda (SGS 1), verificado na API do BCB. Página de metadados do BCB inacessível | Comentário e README corrigidos para descrever a verificação real |
| 2026-10-09 | 03_coletar_clima.py | Sem erro; clima termina em 2026-08 | NASA POWER devolve -999 (sem dado) para 2026-09 e o script descarta o mês | Nenhuma alteração de código; limitação da fonte registrada |
| 2026-10-09 | config.py (09) | Melhor `alpha` do Ridge na borda da grade (100, RMSE 31,50; `alpha`=10 deu 32,54) | A grade {100, 10, 1, 0.1} parava em 100: melhor valor na borda sugere que um valor mais regularizado poderia ser melhor. Conferência feita só com o treino (teste fechado) | Acrescentado `alpha = 1000` (grade {1000, 100, 10, 1, 0.1}). Resultado: 1000 deu RMSE 32,58 (pior); a escolha continua `alpha = 100`, agora no interior da grade, sem efeito na escolha. Regra fixa: grade não será estendida de novo |
| 2026-10-09 | 09_treinar_modelos.py | Decisão do autor: `class_weight="balanced"` na logística e no RF de classificação | Métrica de decisão é macro-F1 e o treino tem 61% de alta; sem o peso o modelo tende a prever quase sempre alta | Aplicado só aos classificadores (Ridge e RF de regressão sem peso); registrado no plan.md (decisão 6) |
| 2026-10-09 | 09_treinar_modelos.py | Validação cruzada com folds desbalanceados (treino de 24, 36 e 48 linhas; folds 2 e 3 só com altas) | `TimeSeriesSplit(3, 12, gap=12)` sobre 72 linhas; macro-F1 por fold indefinido nos folds 2 e 3 | Decisão do autor: nota única sobre as previsões agrupadas dos 3 folds (36 linhas, 6 quedas). Limitação registrada |
| 2026-10-09 | 09_treinar_modelos.py | Macro-F1 do baseline de maioria na validação = 0,14 | Nos folds 2 e 3 o treino tem mais quedas, então a maioria vira "queda" e erra todas as altas. Artefato do desenho dos folds, não erro de código | Nenhuma alteração. No teste o baseline usa o treino inteiro (maioria = alta) e dá macro-F1 0,41 |
| 2026-10-09 | 10_avaliar_modelos.py | Teste aberto uma única vez; 09, grades, variáveis, pesos e tolerâncias congelados depois | Regra do teste (tasks.md e constituição v1.1.0) | Nenhuma alteração no 09 depois da primeira saída do 10. Reprodutibilidade conferida: 12 tabelas com hash idêntico em 2 rodadas |
| 2026-10-09 | Git (processo) | Mensagens dos commits `39e3f77` e `40506ef` defasadas e `b21d0a1` com código do T010 | Erro meu: commit feito na mesma chamada da edição seguinte | Código final correto; mensagens não reescritas |
| 2026-10-09 | tasks.md (processo) | BOM (UTF-8) gravado pelo PowerShell ao marcar tarefas | `Set-Content -Encoding utf8` grava BOM | BOM removido antes do commit; gravação passou a usar UTF-8 sem BOM |
| 2026-10-09 | 11_prever_ilustrativo.py | Previsão pedida também para 2026-10, 2026-11 e 2026-12: não feita | Câmbio, arábica e IPCA só existem até 2026-09; `cambio_medio_var6m/12m`, `arabica_usd_kg_var6m/12m` e `acum12_passado` desses meses exigiriam valores inventados | Só 2026-09 (aprovado). A janela dela já cobre 2026-10 a 2027-09. Refazer quando saírem os dados de outubro em diante |

A linha do `alpha = 1000` do Ridge (conferência de borda) está no mesmo registro.

## 8. Versões das bibliotecas

| Biblioteca | Versão |
|---|---|
| Python | 3.12.2 |
| pandas | 3.0.6 |
| numpy | 2.5.3 |
| scikit-learn | 1.9.1 |
| matplotlib | 3.11.2 |

## 9. Dúvidas pendentes (para o outro chat)

1. **Regressão sem ganho sobre o baseline:** nenhum modelo supera a média do treino (RMSE 37,93 e 38,45 contra 35,04). Como registrar na seção de avaliação? A premissa "RMSE ao menos 10% menor" não foi cumprida.
2. **Mudança de regime:** o teste contém o pico de 82% (2024-05) e a queda de 2025, com câmbio e arábica fora da faixa do treino. Vale discutir como viés temporal na seção 13.
3. **Validação cruzada:** nota agrupada com 6 quedas e fold 1 com 24 linhas. O macro-F1 do baseline de maioria na validação (0,14) é um artefato dos folds; no teste ele é 0,41. Como apresentar?
4. **Persistência do sinal pior que sortear** (acurácia balanceada 0,29): coerente com a reversão após grandes altas (correlação -0,18 com todas as linhas). Interpretar assim?
5. **Coeficientes de sinais opostos** entre logística e Ridge (por exemplo `oni_l6`): só descritivos, com cerca de 10 janelas independentes.
6. **Safra CONAB (H1 e H5):** continuam fora do modelo (limitação).
7. **Previsão para 2026-10 a 2026-12:** só será possível quando saírem os dados de câmbio, arábica e IPCA desses meses. Refazer a previsão ilustrativa nessa ocasião?
8. **Reescrever mensagens de commit** `39e3f77` e `40506ef` (defasadas)? Hoje só afeta o histórico.
