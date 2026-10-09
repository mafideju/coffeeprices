# Feature Specification: Modelagem temporal da variação do IPCA do café moído

**Feature Branch**: `001-modelagem-temporal-cafe`

**Created**: 2026-10-09

**Status**: Draft

**Input**: Fase B do projeto `cafe-ml` (etapas 3 a 5 do CRISP-DM): comparar, com validação temporal rigorosa, baselines, um modelo linear e um modelo de árvores para prever a variação acumulada do IPCA do café moído nos 12 meses seguintes (classificação como foco, regressão como complemento).

## Contexto

O dataset `dados/processados/dataset_mensal.csv` (Fase A, concluída) tem 129 linhas e 49 colunas, mensais, de 2016-01 a 2026-09. O alvo de cada mês t é a variação acumulada do IPCA do café moído de t+1 a t+12: `alvo_alta` (1 = alta, 0 = queda) e `alvo_acum_12m` (%). Os 12 últimos meses (2025-10 a 2026-09) não têm alvo. Os resultados alimentam o relatório acadêmico e nunca podem ser simulados ou inventados.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conjunto fixo de variáveis e divisão temporal sem vazamento (Priority: P1)

O autor quer uma lista fixa de 13 variáveis explicativas, definida pelas hipóteses do relatório (e não por ranking de correlação), e uma divisão temporal em que nenhuma informação do teste influencie o treino.

**Why this priority**: sem variáveis fixas e sem divisão correta, todas as comparações seguintes perdem validade científica. É a base de tudo.

**Independent Test**: preparar os dados e conferir os tamanhos impressos (72 treino, 33 teste), as datas de início e fim de cada parte e a lista exata de variáveis, sem treinar nenhum modelo.

**Acceptance Scenarios**:

1. **Given** o dataset da Fase A, **When** a preparação é executada, **Then** o treino tem 72 linhas com alvo (2016-01 a 2021-12), o intervalo de segurança de 12 meses (2022) é descartado e o teste tem 33 linhas com alvo (2023-01 a 2025-09), com os tamanhos e as datas impressos.
2. **Given** a preparação concluída, **When** as variáveis do modelo são listadas, **Then** aparecem exatamente as 13 variáveis definidas, sem nenhuma outra.
3. **Given** qualquer linha do treino, **When** se observa o período coberto pelo seu alvo (12 meses seguintes), **Then** esse período não invade o teste.

---

### User Story 2 - Comparação de baselines, modelo linear e modelo de árvores (Priority: P1)

O autor quer treinar e comparar, na classificação e na regressão, dois baselines, um modelo linear e um modelo de árvores, para justificar a escolha do modelo no relatório.

**Why this priority**: é o núcleo da pergunta de pesquisa. Sem o comparativo com os baselines não há conclusão.

**Independent Test**: executar a modelagem e verificar que existe uma tabela com os 4 modelos de classificação e os 4 de regressão, cada um com suas métricas, usando só o treino para ajustes.

**Acceptance Scenarios**:

1. **Given** o treino preparado, **When** os baselines são calculados, **Then** existem, na classificação, a classe majoritária do treino e a persistência do sinal (alta se `acum12_passado` > 0) e, na regressão, a média do alvo no treino e a persistência (`acum12_passado` como previsão).
2. **Given** o treino preparado, **When** os modelos são ajustados, **Then** há regressão logística e Ridge (com padronização ajustada só no treino e regularização L2) e Random Forest com profundidade limitada, para classificação e regressão.
3. **Given** os hiperparâmetros a escolher, **When** o ajuste é feito, **Then** usa-se apenas o treino, com validação cruzada temporal e intervalo de 12 meses entre treino e validação.

---

### User Story 3 - Métricas, tabelas e figuras prontas para o relatório (Priority: P1)

O autor quer métricas, tabelas e figuras para o relatório, com os resultados do teste apresentados como indicativos, já que o teste tem apenas 33 linhas (cerca de 3 janelas independentes).

**Why this priority**: sem as saídas prontas o resultado não entra nas seções do relatório.

**Independent Test**: conferir que a tabela comparativa e as figuras existem em `relatorio/tabelas/` e `relatorio/figuras/` e que o teste só aparece uma vez, ao final.

**Acceptance Scenarios**:

1. **Given** os modelos finais definidos apenas com o treino, **When** o teste é avaliado, **Then** o teste é usado uma única vez e nenhuma decisão de variáveis, hiperparâmetros ou modelo depende dele.
2. **Given** os resultados do teste, **When** a tabela é gerada, **Then** ela traz macro-F1, acurácia balanceada e matriz de confusão (classificação) e RMSE e MAE (regressão), comparando cada modelo com seus baselines.
3. **Given** os resultados, **When** a tabela e as figuras são apresentadas, **Then** os resultados do teste vêm marcados como indicativos, com o tamanho do teste (33 linhas) visível.
4. **Given** os modelos linear e de árvores, **When** a importância é calculada, **Then** há coeficientes padronizados do modelo linear e importância das variáveis do Random Forest.

---

### User Story 4 - Previsão ilustrativa para 2026-09 (Priority: P3)

Ao final, e somente se o autor aprovar, o autor quer uma previsão ilustrativa para o mês 2026-09, cujo alvo ainda não existe, claramente marcada como ilustrativa.

**Why this priority**: é um complemento opcional e não responde à pergunta de pesquisa.

**Independent Test**: com a aprovação do autor, verificar que a saída traz a previsão para 2026-09 com o rótulo "ilustrativa" e sem comparação com valor real.

**Acceptance Scenarios**:

1. **Given** o autor aprovou a etapa, **When** a previsão é gerada, **Then** ela usa os modelos já definidos no treino, informa o mês 2026-09 e exibe o rótulo "ilustrativa".
2. **Given** o autor não aprovou, **When** a modelagem termina, **Then** nenhuma previsão para 2026-09 é produzida.

---

### Edge Cases

- O modelo não supera nenhum baseline: o resultado é relatado como está, sem trocar variáveis, métrica, janela ou modelo para melhorá-lo.
- Uma variável da lista fixa tem valor ausente numa linha com alvo: a execução avisa claramente e informa o que foi feito (a decisão deve ser registrada, nunca silenciosa).
- Treino com classes desbalanceadas (61% de alta nas 72 linhas de treino contra cerca de 70% no teste): as métricas escolhidas devem refletir as duas classes, e o baseline "sempre alta" deve aparecer no comparativo.
- Execuções repetidas: o mesmo comando deve produzir os mesmos resultados (sementes fixas).
- Validação cruzada temporal com poucos dados (72 linhas, janelas sobrepostas): o relatório deve registrar a limitação, e o ajuste não pode usar o teste para compensá-la.
- Variáveis fora da lista fixa presentes no dataset (inclusive `oni` sem defasagem e colunas brutas): não podem entrar em nenhum modelo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST usar exatamente 13 variáveis explicativas fixas: `cambio_medio_var6m`, `cambio_medio_var12m`, `arabica_usd_kg_var6m`, `arabica_usd_kg_var12m`, `chuva_anom_l3`, `chuva_anom_l6`, `tempmin_anom_l3`, `tempmin_anom_l6`, `oni_l6`, `oni_l12`, `mes_sen`, `mes_cos` e `acum12_passado`, definidas pelas hipóteses (H2, H3, H4, H6, H7) e não por ranking de correlação.
- **FR-002**: O sistema MUST rejeitar qualquer variável fora dessa lista, inclusive `oni` sem defasagem, colunas brutas, alvos e a coluna `periodo`, e MUST registrar a lista usada na saída.
- **FR-003**: O sistema MUST dividir os dados de forma temporal, sem embaralhar: treino de 2016-01 a 2021-12 (72 linhas com alvo), intervalo de segurança de 12 meses (2022) descartado e teste de 2023-01 a 2025-09 (33 linhas com alvo).
- **FR-004**: O sistema MUST imprimir e verificar os tamanhos (72 e 33) e as datas de início e fim de cada parte, e MUST interromper com mensagem clara se divergirem.
- **FR-005**: O sistema MUST calcular, para classificação, os baselines (i) classe majoritária do treino e (ii) persistência do sinal (prever alta se `acum12_passado` > 0).
- **FR-006**: O sistema MUST calcular, para regressão, os baselines (i) média do alvo no treino e (ii) persistência (`acum12_passado` como previsão).
- **FR-007**: O sistema MUST treinar regressão logística (classificação) e Ridge (regressão), com padronização ajustada só no treino e regularização L2.
- **FR-008**: O sistema MUST treinar Random Forest para classificação e regressão, com profundidade limitada.
- **FR-009**: O ajuste de hiperparâmetros MUST usar apenas o treino, com validação cruzada temporal e intervalo de 12 meses entre treino e validação.
- **FR-010**: O sistema MUST calcular macro-F1, acurácia balanceada e matriz de confusão na classificação, e RMSE e MAE na regressão. O sistema MUST NOT usar MAPE (o alvo cruza zero) nem acurácia simples como métrica principal.
- **FR-011**: O conjunto de teste MUST ser usado uma única vez, ao final, e nenhuma decisão de variáveis, hiperparâmetros ou modelo pode depender dele.
- **FR-012**: O sistema MUST calcular a importância das variáveis: coeficientes padronizados do modelo linear e importância das variáveis do Random Forest.
- **FR-013**: O sistema MUST salvar a tabela comparativa de métricas (cada modelo contra seus baselines) em `relatorio/tabelas/` e as figuras de avaliação e de importância em `relatorio/figuras/`.
- **FR-014**: Os resultados do teste MUST aparecer marcados como indicativos, com o tamanho do teste (33 linhas, cerca de 3 janelas independentes) informado.
- **FR-015**: O sistema MUST usar sementes fixas em tudo que for aleatório, e cada etapa MUST ser executável por script a partir da raiz do projeto.
- **FR-016**: Se os modelos não superarem os baselines, o sistema MUST relatar o resultado como está, sem alterar a metodologia para melhorá-lo.
- **FR-017**: Mediante aprovação explícita do autor, o sistema MUST gerar uma previsão ilustrativa para 2026-09, claramente rotulada como ilustrativa e sem comparação com valor real. Sem a aprovação, MUST NOT gerá-la.
- **FR-018**: O sistema MUST NOT coletar novos dados, criar novas variáveis, ajustar parâmetros usando o teste, usar redes neurais, expor API ou fazer implantação.

### Key Entities

- **Dataset mensal**: 129 linhas × 49 colunas, uma por mês, de 2016-01 a 2026-09, com alvos de classificação e regressão.
- **Conjunto de variáveis fixas**: as 13 variáveis explicativas e a hipótese do relatório que cada uma representa.
- **Partição temporal**: treino (72 linhas), intervalo de segurança (2022, descartado) e teste (33 linhas), com datas de início e fim.
- **Modelo e baseline**: cada um com tarefa (classificação ou regressão), família (baseline, linear ou árvores), hiperparâmetros escolhidos no treino e métricas.
- **Tabela de resultados**: métricas de cada modelo contra seus baselines, com marcação de resultados indicativos.
- **Previsão ilustrativa (opcional)**: valor previsto para 2026-09, com rótulo "ilustrativa".

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A partição impressa mostra exatamente 72 linhas de treino e 33 de teste, com o treino terminando em 2021-12 e o teste indo de 2023-01 a 2025-09, em 100% das execuções.
- **SC-002**: Em 100% dos modelos, o conjunto de variáveis usado coincide exatamente com as 13 definidas, e nenhuma outra aparece.
- **SC-003**: Existe uma tabela comparativa com 4 modelos de classificação e 4 de regressão (2 baselines, 1 linear e 1 de árvores por tarefa), com macro-F1, acurácia balanceada, RMSE e MAE, cada modelo contra seus baselines.
- **SC-004**: Duas execuções consecutivas do pipeline completo produzem tabelas idênticas.
- **SC-005**: O teste é avaliado exatamente uma vez, e a revisão do código não encontra nenhuma decisão (variáveis, hiperparâmetros, modelo) que dependa dele.
- **SC-006**: As tabelas e figuras previstas existem em `relatorio/tabelas/` e `relatorio/figuras/` e podem ser inseridas no relatório sem edição manual dos números.
- **SC-007**: Se algum modelo não superar seu baseline, o resultado aparece nas tabelas e no resumo exatamente assim, sem ajuste posterior de metodologia.

## Assumptions

- A Fase A está concluída e commitada, e o dataset da Fase A não será alterado nesta feature.
- As 13 variáveis já existem no dataset; nenhuma variável nova será criada.
- O treino efetivo tem 72 linhas porque as 12 linhas de 2022 são descartadas para evitar que o alvo de treino invada o teste; o intervalo de segurança de 12 meses decorre do horizonte do alvo.
- O teste é pequeno (33 linhas, cerca de 3 janelas independentes) e as janelas se sobrepõem, então os resultados do teste são indicativos e não conclusivos.
- Os critérios de aceitação "F1 acima do baseline" e "RMSE pelo menos 10% menor que o baseline" foram substituídos pelas métricas macro-F1, acurácia balanceada, RMSE e MAE, definidas nesta especificação com decisão do autor; um resultado modesto mas bem analisado é aceitável.
- scikit-learn é a única nova dependência, permitida pela constituição na fase de modelagem.
- Esta especificação diverge da constituição v1.0.0 (Princípio III) em três pontos: métricas (macro-F1, acurácia balanceada e MAE em vez de F1, acurácia e MAPE), treino até 2021 com intervalo de segurança em 2022 (em vez de treino até 2022) e critérios de aceitação. A constituição deve ser emendada com aprovação do autor antes do planejamento.
- Safra CONAB não está disponível; as hipóteses H1 e H5 ficam não testadas diretamente, e isso é uma limitação.
