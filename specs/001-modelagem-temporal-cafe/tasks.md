---

description: "Tarefas da modelagem temporal (Fase B, scripts 08 a 10)"
---

# Tarefas: Modelagem temporal da variação do IPCA do café moído

**Entrada**: `specs/001-modelagem-temporal-cafe/` (spec.md, plan.md, research.md, data-model.md, quickstart.md)
**Testes**: sem suíte nova. Cada tarefa tem um **comando** e um **resultado esperado** (verificação). As checagens de tamanhos, colunas e NaN ficam dentro dos próprios scripts.

## Regras para todas as tarefas

- Rodar a partir da raiz, no `.venv`: `$env:PYTHONIOENCODING='utf-8'; .\.venv\Scripts\python.exe src\NN_nome.py`.
- Sem classes, sem frameworks, configuração só em `src/config.py`, `SEMENTE = 42`.
- Dados reais. Nenhuma decisão (variáveis, hiperparâmetros, modelo) pode olhar o teste (FR-011).
- Se os modelos não superarem os baselines, relatar como está (FR-016). **Parar e perguntar** antes de qualquer mudança de metodologia.
- **Cada tarefa termina com um commit** (Conventional Commits, em inglês, com o trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`).
- Formato: `- [ ] ID [P?] [História] Descrição com caminho`. `[P]` = pode rodar em paralelo (arquivos diferentes, sem dependência).
- **Regra do teste**: o script 10 pode ser rodado várias vezes enquanto as figuras são ajustadas. Depois da primeira saída do 10, nenhuma alteração no 09, nas grades, nas variáveis, nos pesos de classe ou nas tolerâncias é permitida. Se algo no 09 precisar mudar, **parar e avisar antes**, explicando o motivo. Toda mudança assim é registrada em `docs/registro-de-correcoes.md`.
- **Paradas de revisão** (🛑): mostrar a saída completa e esperar o "pode seguir" do autor.
- Todos os comandos são PowerShell do Windows (sem `grep`, sem `&&`).

---

## Fase 1: Preparação (configuração e dependência)

**Objetivo**: dependência instalada e todos os valores novos em `config.py`.

- [X] T001 Confirmar `scikit-learn` em `requirements.txt` e no `.venv`
  - **Comando**: `.\.venv\Scripts\python.exe -m pip check; .\.venv\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"`
  - **Esperado**: `No broken requirements found.` e `1.9.1`; `requirements.txt` lista `scikit-learn`.
  - **Commit**: `chore: add scikit-learn dependency`

- [X] T002 Adicionar a `src/config.py`: `FEATURES_MODELO` (as 13 variáveis do FR-001, nesta ordem), `SEMENTE = 42`, `N_SPLITS_CV = 3`, `TAMANHO_VALIDACAO_CV = 12`, `TAMANHOS_ESPERADOS = (72, 33)`, grades (logística `C` {0.01, 0.1, 1, 10}; Ridge `alpha` {100, 10, 1, 0.1}, ordenadas do mais simples ao mais complexo; RF `n_estimators = 300`, `max_depth` {2, 3, 4}, `min_samples_leaf` {10, 5}), `TOLERANCIA_MACRO_F1 = 0.03` e `TOLERANCIA_RMSE = 0.03`. Reutilizar `GAP_MESES` e `ANO_FIM_TREINO`. **Pré-requisito** (cumprido): tolerâncias e grades aprovadas pelo autor em 2026-10-09.
  - **Comando**: `.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0,'src'); import config as c; print(len(c.FEATURES_MODELO), set(c.FEATURES_MODELO) <= set(c.FEATURES_CANDIDATAS), c.SEMENTE, c.TAMANHOS_ESPERADOS)"`
  - **Esperado**: `13 True 42 (72, 33)`.
  - **Commit**: `feat: add modeling settings to config`

**Ponto de controle**: o `config.py` importa sem erro; os scripts 01 a 07 continuam funcionando (nada que eles usam foi alterado).

---

## Fase 2: História 1 - Variáveis fixas e divisão temporal sem vazamento (P1)

**Objetivo**: X, y, treino de 72 linhas e teste de 33, verificados e impressos, sem treinar modelo.
**Teste independente**: rodar o 08 e conferir tamanhos, datas e as 13 colunas.

- [X] T003 [US1] Criar `src/08_preparar_modelagem.py`: ler `dados/processados/dataset_mensal.csv`; conferir que as 13 colunas existem e que `oni`, `periodo` e os alvos não estão entre as variáveis (FR-002); treino = `mes <= Timestamp(f"{ANO_FIM_TREINO}-12-01") - GAP_MESES meses` (2021-12) com alvo; teste = `mes >= 2023-01` com alvo (2022 descartado); interromper com mensagem clara se os tamanhos divergirem de `TAMANHOS_ESPERADOS`, se houver NaN nas 13 variáveis ou se `último mês do treino + 12 meses` for >= primeiro mês do teste; gravar `dados/processados/modelagem_treino.csv` e `modelagem_teste.csv` (colunas `mes`, 13 variáveis, `alvo_alta`, `alvo_acum_12m`).
  - **Comando**: `$env:PYTHONIOENCODING='utf-8'; .\.venv\Scripts\python.exe src\08_preparar_modelagem.py`
  - **Esperado**: imprime `treino: 72 linhas (2016-01 a 2021-12)`, `descartado: 2022`, `teste: 33 linhas (2023-01 a 2025-09)`, a lista das 13 variáveis, `0 NaN`; saída 0 e dois CSVs criados.
  - **Commit**: `feat: add modeling data preparation script`

- [X] T004 [US1] Provar que as travas funcionam: rodar o 08 uma vez com `TAMANHOS_ESPERADOS = (73, 33)` (alterado temporariamente, sem commit) e voltar o valor.
  - **Comando**: igual ao de T003, após a edição temporária.
  - **Esperado**: o script para com mensagem clara dizendo que o treino tem 72 e não 73; depois de reverter, T003 volta a passar. `git diff src\config.py` vazio.
  - **Commit**: nenhum (verificação; não deixa alteração).

- [ ] 🛑 PARADA A (depois do T004): colar a saída completa do script 08 (72, 33, 0 NaN, 13 variáveis) e esperar o "pode seguir". Não começar o T005 antes.

**Ponto de controle (SC-001, SC-002)**: 72 e 33 impressos; só as 13 variáveis.

---

## Fase 3: História 2 - Baselines, modelo linear e Random Forest (P1)

**Objetivo**: ajustar e escolher hiperparâmetros só com o treino, validação cruzada temporal com intervalo de 12 meses.
**Teste independente**: rodar o 09 e conferir as divisões impressas, a tabela de validação e os hiperparâmetros escolhidos; o arquivo do teste não pode ser aberto.

- [ ] T005 [US2] Criar `src/09_treinar_modelos.py` (parte 1: leitura e divisões): ler **somente** `modelagem_treino.csv`; criar `TimeSeriesSplit(n_splits=N_SPLITS_CV, test_size=TAMANHO_VALIDACAO_CV, gap=GAP_MESES)`; imprimir por divisão: tamanho de treino e de validação, período e contagem de classes; avisar se algum treino tiver menos de 30 linhas e **parar com mensagem clara** se algum treino tiver uma só classe.
  - **Comando**: `$env:PYTHONIOENCODING='utf-8'; .\.venv\Scripts\python.exe src\09_treinar_modelos.py`
  - **Esperado**: 3 divisões impressas: treino 24, 36, 48; validação 12, 12, 12 (2019, 2020, 2021); alta na validação 6, 12, 12; aviso de que a divisão 1 treina com poucas linhas.
  - **Commit**: `feat: add temporal cross-validation splits`

- [ ] T006 [US2] No `09`, baselines (parte 2): classificação (i) classe majoritária do treino e (ii) persistência (alta se `acum12_passado > 0`); regressão (i) média do alvo no treino e (ii) `acum12_passado` como previsão. Calcular a nota agrupada das previsões de validação das 3 divisões (macro-F1 com `labels=[0,1]` e `zero_division=0`; RMSE) e gravar em `relatorio/tabelas/validacao_cruzada.csv` (colunas `tarefa`, `modelo`, `hiperparametros`, `nota`, `escolhida`). Guardar no `modelos_treinados.joblib` apenas o que o 10 precisa dos baselines (classe majoritária e média, ambos calculados nas 72 linhas do treino). **Antes de calcular a persistência da regressão**, conferir que `acum12_passado` e `alvo_acum_12m` estão na mesma unidade (percentual, não fração): imprimir uma linha de exemplo (mês e valor das duas colunas) e a faixa mínima e máxima de cada uma no treino; se as escalas divergirem, parar com mensagem clara.
  - **Comando**: igual ao de T005.
  - **Esperado**: linha de exemplo e faixas das duas colunas impressas, na mesma unidade (percentual); se divergirem, o script para com mensagem clara. 4 linhas de baseline na tabela (2 de classificação, 2 de regressão); a classe majoritária prevê "alta" nas 3 divisões; notas impressas.
  - **Commit**: `feat: add baseline models and scores`

- [ ] T007 [US2] No `09`, modelo linear (parte 3): `Pipeline([StandardScaler, LogisticRegression(penalty L2, class_weight="balanced", random_state=SEMENTE)])` varrendo `C` e `Pipeline([StandardScaler, Ridge])` varrendo `alpha` (Ridge sem peso de classe); para cada configuração, ajustar em cada divisão, **juntar** as previsões de validação e calcular uma única nota (macro-F1 ou RMSE); aplicar a regra de desempate (primeira configuração, da mais simples, dentro de `TOLERANCIA_MACRO_F1` ou `TOLERANCIA_RMSE` da melhor); reajustar a escolhida nas 72 linhas; registrar em `validacao_cruzada.csv` e `hiperparametros_escolhidos.csv`.
  - **Comando**: igual ao de T005.
  - **Esperado**: 4 configurações por modelo na tabela, uma marcada `escolhida`; `hiperparametros_escolhidos.csv` com 2 linhas lineares; nenhuma leitura de `modelagem_teste.csv` (`Select-String -Path src\09_treinar_modelos.py -Pattern "modelagem_teste"` não retorna nada); `hiperparametros_escolhidos.csv` mostra `class_weight=balanced` só na logística.
  - **Commit**: `feat: add linear models with temporal tuning`

- [ ] T008 [US2] No `09`, Random Forest (parte 4): `Pipeline([StandardScaler, RandomForestClassifier(n_estimators=300, class_weight="balanced", max_depth, min_samples_leaf, random_state=SEMENTE) / RandomForestRegressor(n_estimators=300, max_depth, min_samples_leaf, random_state=SEMENTE)])` (regressor sem peso) varrendo `max_depth` e `min_samples_leaf`; mesma nota agrupada e mesma regra de desempate; gravar `modelos_treinados.joblib` (4 pipelines finais mais os parâmetros dos baselines), `validacao_cruzada.csv` e `hiperparametros_escolhidos.csv` completos.
  - **Comando**: `1..2 | ForEach-Object { .\.venv\Scripts\python.exe src\09_treinar_modelos.py | Out-Null; (Get-FileHash relatorio\tabelas\validacao_cruzada.csv).Hash; (Get-FileHash relatorio\tabelas\hiperparametros_escolhidos.csv).Hash }`
  - **Esperado**: 6 configurações de RF por tarefa; `hiperparametros_escolhidos.csv` com 4 linhas e `class_weight=balanced` só nos classificadores; os dois pares de hashes **idênticos** nas duas execuções (SC-004).
  - **Commit**: `feat: add random forest with temporal tuning`

- [ ] 🛑 PARADA B (depois do T008, ANTES do T009): colar a saída completa do 09 (tamanhos e classes por divisão, tabela de validação cruzada, hiperparâmetros escolhidos, verificação de escala) e esperar o "pode seguir". **O teste só é aberto depois desta parada.**

**Ponto de controle (FR-009)**: tudo ajustado só com o treino; hiperparâmetros escolhidos e registrados antes de o teste ser aberto.

---

## Fase 4: História 3 - Avaliação no teste, tabelas e figuras (P1)

**Objetivo**: o teste lido uma única vez, métricas e figuras prontas para o relatório.
**Teste independente**: rodar o 10 e conferir tabelas e figuras; `Select-String` mostra que só o 10 lê `modelagem_teste.csv`.
**Regra do teste**: o 10 pode ser rodado várias vezes enquanto as figuras são ajustadas, mas depois da primeira saída do 10 nada no 09, nas grades, nas variáveis, nos pesos de classe ou nas tolerâncias pode mudar. Se algo precisar mudar, parar e avisar antes, explicando o motivo, e registrar em `docs/registro-de-correcoes.md`.
**Pré-requisito**: PARADA B aprovada.

- [ ] T009 [US3] Criar `src/10_avaliar_modelos.py` (parte 1: métricas): carregar `modelos_treinados.joblib`; ler `modelagem_teste.csv` (único ponto do projeto que o lê); aplicar os 4 modelos de cada tarefa (persistência calculada na hora a partir de `acum12_passado`); gravar `metricas_classificacao.csv` (modelo, macro-F1, acurácia balanceada, VN, FP, FN, VP, `n_teste`) e `metricas_regressao.csv` (modelo, RMSE, MAE, `n_teste`) e `previsoes_teste.csv`. Sem MAPE e sem acurácia simples. Imprimir o aviso "resultados indicativos: teste com 33 linhas (cerca de 3 janelas independentes)".
  - **Comando**: `$env:PYTHONIOENCODING='utf-8'; .\.venv\Scripts\python.exe src\10_avaliar_modelos.py`
  - **Esperado**: `n_teste = 33` em todas as linhas; 4 linhas em cada métrica; baseline "sempre alta" com acurácia balanceada 0,50 e macro-F1 ≈ 0,41; `previsoes_teste.csv` com 33 linhas. `Select-String -Path src\*.py -Pattern modelagem_teste` aponta só o 08 (grava) e o 10 (lê).
  - **Commit**: `feat: add test evaluation metrics`

- [ ] T010 [US3] No `10`, importância das variáveis: coeficientes padronizados da logística e do Ridge (valores direto do `Pipeline`, já em escala padronizada) e `feature_importances_` dos dois Random Forest; gravar `importancia_variaveis.csv` (tarefa, modelo, variável, valor).
  - **Comando**: igual ao de T009.
  - **Esperado**: 4 modelos × 13 variáveis = 52 linhas, só as 13 variáveis; importâncias do RF somam 1 por modelo.
  - **Commit**: `feat: add feature importance table`

- [ ] T011 [P] [US3] No `10`, figuras `relatorio/figuras/09_comparacao_modelos.png` (macro-F1 e acurácia balanceada; RMSE e MAE, cada modelo contra seus baselines) e `10_matrizes_confusao.png` (4 modelos), ambas com a nota "resultados indicativos: teste com 33 linhas".
  - **Comando**: igual ao de T009.
  - **Esperado**: os 2 PNGs existem, abrem e trazem a nota; rodar duas vezes não muda as tabelas.
  - **Commit**: `feat: add model comparison and confusion matrix figures`

- [ ] T012 [P] [US3] No `10`, figuras `11_previsto_vs_real.png` (regressão, 33 meses, com o real e a previsão de cada modelo) e `12_importancia_variaveis.png` (coeficientes e importância do RF), com a nota de resultados indicativos.
  - **Comando**: igual ao de T009.
  - **Esperado**: os 2 PNGs existem; as 4 figuras `09_` a `12_` estão em `relatorio/figuras/`.
  - **Commit**: `feat: add predicted vs actual and importance figures`

- [ ] T013 [US3] Rodar o pipeline completo duas vezes (08, 09 e 10) e comparar as tabelas.
  - **Comando**: `$scripts = '08_preparar_modelagem','09_treinar_modelos','10_avaliar_modelos'; 1..2 | ForEach-Object { foreach ($s in $scripts) { .\.venv\Scripts\python.exe "src\$s.py" | Out-Null }; Get-FileHash relatorio\tabelas\*.csv | Select-Object Hash, @{n='Arquivo';e={Split-Path $_.Path -Leaf}} }`
  - **Esperado**: hashes idênticos entre as duas rodadas (SC-004). É só conferência de reprodutibilidade, sem alterar código; se divergirem, parar e avisar.
  - **Commit**: `chore: add model tables and figures` (inclui `relatorio/tabelas/` e `relatorio/figuras/` novos)

**Ponto de controle (SC-003, SC-005, SC-006, SC-007)**: tabelas comparativas de 4 modelos por tarefa, cada um contra seus baselines; resultados registrados exatamente como saíram.

---

## Fase 5: História 4 - Previsão ilustrativa para 2026-09 (P3, opcional)

**Só executar se o autor aprovar explicitamente depois de ver os resultados (FR-017).** Sem aprovação, nenhuma tarefa desta fase é feita e nenhum arquivo é criado.

- [ ] T014 [US4] (condicional) Criar `src/11_prever_ilustrativo.py`: usar os modelos já escolhidos no treino, montar as 13 variáveis de 2026-09 e gravar `relatorio/tabelas/previsao_ilustrativa_2026-09.csv` com o rótulo "ilustrativa" e sem valor real.
  - **Comando**: `$env:PYTHONIOENCODING='utf-8'; .\.venv\Scripts\python.exe src\11_prever_ilustrativo.py`
  - **Esperado**: 1 linha por modelo, mês 2026-09, coluna `rotulo = ilustrativa`; sem NaN nas 13 variáveis (hoje o ONI e o clima terminam em 2026-08; as defasagens usadas já cobrem 2026-09).
  - **Commit**: `feat: add illustrative 2026-09 forecast`

---

## Fase 6: Fechamento (registro, pacote de retorno, publicação)

- [ ] T015 Registrar em `docs/registro-de-correcoes.md` o que foi decidido e corrigido na Fase B (nota agrupada da validação, desempate, tolerâncias, `class_weight="balanced"`, qualquer mudança no 09 depois da primeira saída do 10, qualquer ajuste feito durante a implementação, e a limitação "6 meses de queda na nota agrupada").
  - **Comando**: `git diff --stat docs\registro-de-correcoes.md`
  - **Esperado**: entradas novas datadas, em português.
  - **Commit**: `docs: log phase B decisions and corrections`

- [ ] T016 Atualizar `docs/resumo.md` e `docs/pacote-de-retorno.md` com a Fase B e **criar `docs/pacote-de-retorno-faseb.md`**. Conteúdo obrigatório do novo arquivo, colando a saída real, sem resumir nem inventar números: saída completa dos scripts 08, 09 e 10; tabelas de métricas (classificação e regressão) e de importância das variáveis; hiperparâmetros escolhidos e tabela de validação cruzada; tamanhos e contagem de classes de cada divisão da validação cruzada; lista das figuras geradas; correções feitas (`docs/registro-de-correcoes.md`); versões das bibliotecas (Python, pandas, numpy, scikit-learn, matplotlib); dúvidas pendentes. Nos outros dois arquivos: variáveis usadas, tamanhos, hiperparâmetros, limitações (teste de 33 linhas, nota agrupada com 6 quedas, divisão 1 com 24 linhas, H1 e H5 não testadas) e a conclusão sobre baselines, exatamente como saiu.
  - **Comando**: `Test-Path docs\pacote-de-retorno-faseb.md; Select-String -Path docs\pacote-de-retorno-faseb.md -Pattern "macro-F1","RMSE" | Select-Object -First 5`
  - **Esperado**: `True`; números iguais aos de `metricas_*.csv` (conferir por amostragem); nenhum valor inventado.
  - **Commit**: `docs: add phase B return package (docs/pacote-de-retorno-faseb.md) and update summary`

- [ ] T017 Marcar as tarefas concluídas neste `tasks.md`, conferir `git status` limpo e `git log --oneline` com um commit por tarefa; lembrar o autor de rodar `git push` (o ambiente não faz login interativo).
  - **Comando**: `git status --short; git --no-pager log --oneline -20`
  - **Esperado**: árvore limpa; commits em Conventional Commits.
  - **Commit**: `docs: mark phase B tasks as completed`

---

## Dependências e ordem

```text
T001 → T002 → T003 → (T004) → 🛑A → T005 → T006 → T007 → T008 → 🛑B → T009 → T010 → (T011, T012 em paralelo) → T013 → [T014 opcional] → T015 → T016 → T017
```

- T011 e T012 mexem em partes diferentes do script 10 e só dependem de T010; na prática, como o arquivo é o mesmo, rodar em sequência é mais seguro.
- `09` depende só do treino; `10` depende do `09` e do teste. Nada no `09` pode ler o arquivo do teste.

## Estratégia

- **MVP**: T001 a T013 (histórias 1 a 3, todas P1). A história 4 e o fechamento vêm depois.
- Parar para mostrar a saída ao autor ao fim de cada fase; **parar e perguntar** antes de qualquer mudança de variáveis, divisão, métricas ou grades.
