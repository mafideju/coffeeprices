<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles: II (esclarecimento da climatologia); III (divisão com intervalo
de segurança, métricas de decisão e critério de aceitação)
Added sections: nenhuma
Removed sections: nenhum
Follow-up TODOs: nenhum.
-->

# Constituição do Projeto Café

## Core Principles

### I. Dados Reais e Reprodutibilidade
O projeto MUST usar dados reais obtidos de fontes identificáveis. É proibido inventar,
simular ou mockar dados e resultados apresentados como reais. As coletas e transformações
MUST ser reproduzíveis; quando houver aleatoriedade, MUST usar sementes fixas.

### II. Integridade Temporal e Ausência de Vazamento
Cada variável explicativa MUST usar somente informação disponível até o mês previsto.
O alvo MUST representar a variação acumulada do IPCA do café moído entre t+1 e t+12.
O ONI MUST usar defasagem mínima de dois meses. Anomalias climáticas MUST usar médias
calculadas somente até `ANO_FIM_TREINO`, nunca com dados do teste. Nenhuma etapa pode usar informação futura como
entrada do modelo.

### III. Validação Temporal e Baseline Obrigatório
A divisão entre treino e teste MUST respeitar o tempo e nunca embaralhar as observações:
treino de 2016-01 a 2021-12, intervalo de segurança de 12 meses (2022, descartado) e teste
de 2023-01 em diante. O intervalo existe porque o alvo olha 12 meses à frente: sem ele, o
alvo das últimas linhas de treino cairia dentro do teste. Na modelagem, o tamanho do
intervalo vem de `GAP_MESES` em `src/config.py`. `ANO_FIM_TREINO` (2022) continua sendo
usado apenas na coluna `periodo` e na climatologia das anomalias (Princípio II), e MUST NOT
definir o treino da modelagem. Ajustes de hiperparâmetros MUST usar validação temporal com
o mesmo intervalo, apenas sobre o treino. O teste MUST ser usado uma única vez, ao final.

Todo modelo MUST ser comparado com baselines. As métricas de decisão são: macro-F1 e
acurácia balanceada na classificação; RMSE e MAE na regressão. MAPE e acurácia simples
MUST NOT ser métricas de decisão, porque o alvo cruza zero e as classes são desbalanceadas
no teste. Se um modelo não superar os baselines, o resultado MUST ser relatado como está,
sem alterar a metodologia para melhorá-lo. Um resultado modesto, porém bem analisado, é
aceitável.

### IV. Simplicidade e Configuração Central
O código MUST preferir soluções curtas, legíveis e adequadas a quem está começando em
Python e Machine Learning, sem abstrações ou dependências desnecessárias. As configurações
compartilhadas, incluindo caminhos, períodos, URLs e identificadores de séries, MUST ficar
em `src/config.py`; scripts não devem duplicar esses valores. Cada script de etapa MUST
poder ser executado da raiz do projeto com `python src/NN_nome.py`. Segredos MUST ficar
fora do código.

### V. Spec-Driven Development e Mudanças Controladas
O trabalho de implementação MUST seguir os artefatos e o fluxo Spec Kit acordados. Mudanças
na definição do alvo, divisão temporal, variáveis, modelos, métricas ou período de análise
MUST ser apresentadas ao autor e aprovadas antes de serem aplicadas. Cada correção MUST
ser registrada em `docs/registro-de-correcoes.md` e ter seu próprio commit Conventional
Commits, com tipo e descrição em inglês.

## Additional Constraints

Os dados são mensais, de nível nacional, cobrindo o período definido em `src/config.py`.
As dependências MUST permanecer mínimas: pandas, numpy, requests, matplotlib e openpyxl
para coleta e análise; scikit-learn somente na fase de modelagem. A inclusão de nova
dependência exige justificativa. Resultados, limitações, ausências e problemas de qualidade
das fontes MUST ser descritos com transparência. Correlações com alvos de janelas futuras
sobrepostas não podem ser apresentadas como evidência causal.

## Development Workflow

Os scripts de coleta e análise MUST ser executados individualmente e na ordem documentada
no README. A saída de cada etapa MUST ser inspecionada e validada antes de iniciar a
seguinte. Correções devem ser mínimas, baseadas em evidência da fonte ou do arquivo real,
e acompanhadas do registro definido no princípio V. Antes de concluir uma alteração,
devem ser executadas as verificações existentes mais específicas que cubram o comportamento
alterado. Antes de interpretar respostas externas, deve-se conferir a documentação oficial
e inspecionar o formato realmente retornado, inclusive se for XML em vez de JSON.

## Governance

Esta constituição governa as decisões do projeto e deve ser consultada ao especificar,
planejar, implementar ou revisar mudanças. Alterações a ela exigem justificativa e aprovação
do autor. A versão segue SemVer: MAJOR para mudanças incompatíveis nas regras, MINOR para
novos princípios ou requisitos materiais e PATCH para esclarecimentos sem mudança de sentido.
A conformidade deve ser revisada em cada mudança relevante e antes de seu commit. Qualquer
conflito entre uma alteração proposta e as regras metodológicas deve ser levado ao autor
antes da implementação.

**Version**: 1.1.0 | **Ratified**: 2026-10-09 | **Last Amended**: 2026-10-09
