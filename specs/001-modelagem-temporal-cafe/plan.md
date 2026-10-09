# Implementation Plan: Modelagem temporal da variação do IPCA do café moído

**Branch**: `001-modelagem-temporal-cafe` | **Date**: 2026-10-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-modelagem-temporal-cafe/spec.md`

## Summary

Três scripts numerados (`08`, `09`, `10`), no mesmo estilo da Fase A, comparam baselines, um modelo linear e um Random Forest para classificação (`alvo_alta`, foco) e regressão (`alvo_acum_12m`, complemento). O `08` monta X e y e a divisão temporal e confere 72 e 33 linhas. O `09` escolhe hiperparâmetros só com o treino, por validação cruzada temporal com intervalo de 12 meses. O `10` avalia o teste uma única vez e gera tabelas e figuras. Tudo é configurado em `src/config.py`, sem classes nem camadas extras.

## Technical Context

**Language/Version**: Python 3.12.2, no `.venv` existente

**Primary Dependencies**: pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2 (já instalados); scikit-learn 1.9.1 (adicionado a `requirements.txt` e instalado; `pip check` sem conflitos). `joblib` e `scipy` vêm como dependências do scikit-learn.

**Storage**: arquivos CSV e um arquivo `joblib` em `dados/processados/` (fora do Git); tabelas e figuras em `relatorio/`

**Testing**: sem suíte nova. Verificações dentro dos próprios scripts (tamanhos 72 e 33, lista exata de 13 variáveis, ausência de NaN, treino sem sobreposição com o teste) e roteiro de validação em `quickstart.md`

**Target Platform**: Windows, PowerShell, terminal do PyCharm, execução com `python src/NN_nome.py` a partir da raiz

**Project Type**: scripts de análise (pipeline em lote, sem interface)

**Performance Goals**: pipeline completo em poucos minutos (72 linhas e 13 variáveis; grades pequenas)

**Constraints**: sem classes, frameworks ou camadas extras; configuração só em `config.py`; `random_state = 42`; execuções repetidas produzem tabelas idênticas

**Scale/Scope**: 72 linhas de treino, 33 de teste, 13 variáveis; 8 modelos (2 baselines, 1 linear e 1 de árvores, para duas tarefas)

## Constitution Check

*GATE: avaliado antes da pesquisa e reavaliado após o desenho. Constituição v1.1.0.*

| Princípio | Verificação | Resultado |
|---|---|---|
| I. Dados reais e reprodutibilidade | Só o dataset real da Fase A; `SEMENTE = 42` em todo componente aleatório | Passa |
| II. Ausência de vazamento | 13 variáveis fixas, todas de passado; `oni` sem defasagem fora; padronização dentro do `Pipeline`, ajustada só nos dados de treino de cada divisão | Passa |
| III. Validação temporal e baseline | Treino 2016-01 a 2021-12, intervalo de 12 meses (2022), teste de 2023-01 em diante; `TimeSeriesSplit(gap=GAP_MESES)`; macro-F1, acurácia balanceada, RMSE, MAE; dois baselines por tarefa; teste usado uma única vez (no `10`) | Passa |
| IV. Simplicidade e configuração central | Funções simples, sem classes; novos valores só em `config.py`; scikit-learn é a dependência permitida na modelagem | Passa |
| V. SDD e mudanças controladas | A regra de nota da validação cruzada e as tolerâncias de desempate foram decididas pelo autor (ver "Decisões registradas"); o peso das classes foi decidido pelo autor (decisão 6) | Passa |

Sem violações; a tabela de Complexity Tracking não se aplica. Reavaliação após o desenho: sem mudança.

## Decisões registradas (autor, 2026-10-09)

1. **Divisões da validação cruzada.** `TimeSeriesSplit(n_splits=3, test_size=12, gap=GAP_MESES)` sobre as 72 linhas de treino produz:

   | Divisão | Treino | Validação | Alta na validação |
   |---|---|---|---|
   | 1 | 24 linhas (2016-01 a 2017-12) | 2019-01 a 2019-12 | 6 de 12 |
   | 2 | 36 linhas (2016-01 a 2018-12) | 2020-01 a 2020-12 | 12 de 12 |
   | 3 | 48 linhas (2016-01 a 2019-12) | 2021-01 a 2021-12 | 12 de 12 |

   Nas divisões 2 e 3 só existe a classe "alta", então o macro-F1 por divisão é indefinido, e a divisão 1 treina com apenas 24 linhas.
2. **Nota única por previsões fora da amostra agrupadas.** As previsões de validação das 3 divisões (36 linhas: 30 de alta e 6 de queda) são juntadas, e calcula-se um único macro-F1 (classificação) e um único RMSE (regressão). Não se faz média por divisão. Limitação a citar no relatório: a nota agrupada se apoia em apenas 6 meses de queda.
3. **Impressão obrigatória por divisão:** tamanho de treino e de validação e contagem de classes de cada uma. Se algum treino de divisão tiver uma só classe, o script imprime um AVISO e para com mensagem clara.
4. **Regra de desempate (preferir o mais simples).** As grades são listadas do mais simples ao mais complexo. Escolhe-se a primeira configuração cuja nota esteja dentro da tolerância da melhor: macro-F1 até `TOLERANCIA_MACRO_F1` abaixo do melhor, ou RMSE até `TOLERANCIA_RMSE` (relativa) acima do melhor. Ordem de simplicidade: regressão logística, `C` crescente (mais regularizada primeiro); Ridge, `alpha` decrescente (mais regularizado primeiro); Random Forest, `max_depth` crescente e, em empate, `min_samples_leaf` decrescente.
5. **Tolerâncias e grades (aprovadas pelo autor em 2026-10-09):** `TOLERANCIA_MACRO_F1 = 0.03` e `TOLERANCIA_RMSE = 0.03` (3% relativo), e as grades do T002. Equivalem aproximadamente ao efeito de uma única previsão errada em 36 linhas, e foram fixadas antes de ver qualquer resultado.
7. **Grade do Ridge ampliada (decisão do autor, 2026-10-09, feita só com o treino).** Na primeira rodada o melhor `alpha` ficou na borda (100), então se acrescentou `alpha = 1000`: grade {1000, 100, 10, 1, 0.1}, do mais simples ao mais complexo. Regra fixa: a grade não será estendida de novo, mesmo que 1000 seja o melhor; nesse caso só se registra que a escolha ficou na borda.6. **Peso das classes (decisão do autor).** `class_weight="balanced"` na `LogisticRegression` e no `RandomForestClassifier`. Não se aplica a Ridge nem ao `RandomForestRegressor`. Motivo: a métrica de decisão é macro-F1 e o treino tem 61% de alta; sem o peso, o modelo tende a prever quase sempre "alta". O peso é recalculado em cada divisão da validação cruzada, só com o treino daquela divisão. Os baselines não mudam.
## Project Structure

### Documentation (this feature)

```text
specs/001-modelagem-temporal-cafe/
├── plan.md              # Este arquivo
├── research.md          # Decisões técnicas (Fase 0)
├── data-model.md        # Entidades e arquivos (Fase 1)
├── quickstart.md        # Roteiro de execução e validação (Fase 1)
└── tasks.md             # Gerado depois por /speckit-tasks
```

Não há `contracts/`: o projeto é um pipeline interno sem interface externa. Os formatos dos arquivos de saída estão em `data-model.md`.

### Source Code (repository root)

```text
src/
├── config.py                  # + FEATURES_MODELO, SEMENTE, grades, tolerâncias (existente)
├── 08_preparar_modelagem.py   # X, y e divisão temporal; confere 72 e 33
├── 09_treinar_modelos.py      # baselines, linear e RF; validação cruzada temporal
└── 10_avaliar_modelos.py      # teste (uma vez), tabelas e figuras

dados/processados/             # fora do Git
├── modelagem_treino.csv       # saída do 08
├── modelagem_teste.csv        # saída do 08; lido só pelo 10
└── modelos_treinados.joblib   # saída do 09

relatorio/tabelas/             # metricas_classificacao.csv, metricas_regressao.csv,
                               # importancia_variaveis.csv, previsoes_teste.csv,
                               # validacao_cruzada.csv, hiperparametros_escolhidos.csv
relatorio/figuras/             # 09_comparacao_modelos.png, 10_matrizes_confusao.png,
                               # 11_previsto_vs_real.png, 12_importancia_variaveis.png
```

**Structure Decision**: estrutura plana existente (`src/NN_nome.py`), sem pacotes, classes ou camadas. Cada script roda sozinho e se comunica com o seguinte por arquivos, como na Fase A. O teste vive em arquivo separado, lido apenas pelo `10`, o que torna verificável o requisito de usar o teste uma única vez.

## Fluxo dos scripts

**08_preparar_modelagem.py**
1. Lê `dataset_mensal.csv`; confere que as 13 colunas de `FEATURES_MODELO` existem.
2. Treino: `mes <= ANO_FIM_TREINO-12 menos GAP_MESES` (2021-12) com alvo; teste: `mes >= ANO_FIM_TREINO+1-01` (2023-01) com alvo; 2022 descartado.
3. Imprime tamanhos e datas e interrompe se divergirem de 72 e 33, se houver NaN nas 13 variáveis ou se o último alvo do treino invadir o teste.
4. Grava `modelagem_treino.csv` e `modelagem_teste.csv` (`mes`, 13 variáveis, `alvo_alta`, `alvo_acum_12m`).

**09_treinar_modelos.py** (lê só o treino)
1. Imprime, por divisão do `TimeSeriesSplit`, tamanhos de treino e validação e contagem de classes; avisa se alguma divisão ficar muito pequena ou se algum treino tiver uma só classe.
2. Para cada configuração das grades, ajusta um `Pipeline(StandardScaler, modelo)` em cada divisão (logística e Random Forest de classificação com `class_weight="balanced"`), junta as previsões de validação e calcula macro-F1 (classificação) ou RMSE (regressão) uma única vez.
3. Aplica a regra de desempate, reajusta cada escolha em todas as 72 linhas de treino e grava `modelos_treinados.joblib`, `validacao_cruzada.csv` e `hiperparametros_escolhidos.csv`.
4. Os baselines não têm hiperparâmetros. O `09` calcula a nota deles na validação, depois de conferir que `acum12_passado` e `alvo_acum_12m` estão na mesma unidade (percentual): imprime uma linha de exemplo e a faixa de cada coluna no treino e para se as escalas divergirem. O `10` os aplica ao teste.

**10_avaliar_modelos.py** (lê o teste pela primeira e única vez)
1. Carrega os modelos; calcula os baselines com o treino: classe majoritária, persistência do sinal (`acum12_passado > 0`), média do alvo e persistência (`acum12_passado`).
2. Prevê o teste e calcula macro-F1, acurácia balanceada e matriz de confusão (classificação) e RMSE e MAE (regressão).
3. Calcula coeficientes padronizados (linear) e importância do Random Forest.
4. Grava as tabelas e as quatro figuras, com o aviso "resultados indicativos: teste com 33 linhas (cerca de 3 janelas independentes)" nos gráficos e tabelas.
5. Regra do teste: o `10` pode ser rodado várias vezes enquanto as figuras são ajustadas. Depois da primeira saída do `10`, nada no `09`, nas grades, nas variáveis, nos pesos ou nas tolerâncias pode mudar sem parar e avisar o autor; qualquer mudança é registrada em `docs/registro-de-correcoes.md`.
## Fora deste plano

A previsão ilustrativa de 2026-09 (história 4, prioridade P3) só será planejada se o autor aprovar ao final, em script separado.
