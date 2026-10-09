# Roteiro de execução e validação

## Pré-requisitos

- Fase A concluída: `dados/processados/dataset_mensal.csv` com 129 linhas e 49 colunas.
- `.venv` ativo; scikit-learn instalado (`pip install -r requirements.txt`; `pip check` limpo).
- Execução sempre a partir da raiz do projeto.

## Execução

```powershell
python src/08_preparar_modelagem.py
python src/09_treinar_modelos.py
python src/10_avaliar_modelos.py
```

## Resultados esperados e verificações

**Após o 08**
- Impressão: treino 72 linhas (2016-01 a 2021-12) e teste 33 linhas (2023-01 a 2025-09); 2022 descartado.
- Lista com exatamente as 13 variáveis; nenhum valor ausente.
- Arquivos `modelagem_treino.csv` e `modelagem_teste.csv` criados.
- Se os tamanhos divergirem, o script para com mensagem clara.

**Após o 09**
- Impressão, por divisão da validação cruzada, de tamanhos de treino e validação e contagem de classes (esperado: 24/36/48 de treino; validação de 12; classes de validação 6-6, 0-12, 0-12), com avisos sobre divisões pequenas.
- Tabela de notas agrupadas por configuração e configuração escolhida pela regra de desempate.
- `modelos_treinados.joblib`, `validacao_cruzada.csv` e `hiperparametros_escolhidos.csv` criados.
- O 09 não lê `modelagem_teste.csv`.

**Após o 10**
- `metricas_classificacao.csv` e `metricas_regressao.csv` com 4 modelos cada, `n_teste = 33`.
- `importancia_variaveis.csv` e `previsoes_teste.csv`.
- Figuras `09_` a `12_` com a nota de resultados indicativos.
- Se algum modelo não superar seu baseline, aparece assim nas tabelas, sem ajuste posterior.

## Verificação de reprodutibilidade

Rodar `08`, `09` e `10` duas vezes e comparar as tabelas de `relatorio/tabelas/`: devem ser idênticas.

```powershell
Get-FileHash relatorio\tabelas\metricas_*.csv
```

## Verificação de ausência de vazamento

- O `09` não referencia o arquivo de teste.
- O `10` é o único script que lê `modelagem_teste.csv`, e o lê uma vez.
- Nenhuma coluna fora das 13 aparece em `modelagem_treino.csv` além de `mes` e dos alvos.
