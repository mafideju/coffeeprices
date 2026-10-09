<!--
Sync Impact Report
Version change: template sem versão de governança -> 1.0.0
Modified principles: nenhum (constituição inicial)
Added sections: Restrições de Dados e Metodologia; Fluxo de Desenvolvimento
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
calculadas somente no período de treino. Nenhuma etapa pode usar informação futura como
entrada do modelo.

### III. Validação Temporal e Baseline Obrigatório
A divisão entre treino e teste MUST respeitar o tempo: treino até 2022 e teste nos anos
seguintes. É proibido embaralhar as observações. Ajustes de hiperparâmetros MUST usar
validação temporal. Todo modelo MUST ser comparado a um baseline. A classificação MUST
ser avaliada por F1-score e acurácia; a regressão, por RMSE e MAPE. Os critérios de
aceitação definidos para este trabalho são F1 acima do baseline e RMSE pelo menos 10%
menor que o baseline; resultados que não atinjam esses critérios MUST ser relatados sem
ser ocultados ou reinterpretados como sucesso.

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

**Version**: 1.0.0 | **Ratified**: 2026-10-09 | **Last Amended**: 2026-10-09
