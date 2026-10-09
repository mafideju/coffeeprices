# Pesquisa e decisões técnicas

Nenhum item ficou como "NEEDS CLARIFICATION". As decisões abaixo foram tomadas pelo autor ou derivam da especificação e da constituição v1.1.0.

## 1. Compatibilidade do scikit-learn
- **Decisão**: scikit-learn 1.9.1, instalado no `.venv` e acrescentado a `requirements.txt`.
- **Evidência**: `pip install --dry-run` não reportou conflito (usa o numpy 2.5.3 já instalado e não toca no pandas 3.0.6); depois da instalação, `pip check` retornou "No broken requirements found". Dependências novas: scipy 1.18.1, joblib 1.6.0, threadpoolctl, narwhals e cloudpickle.
- **Alternativas**: statsmodels (rejeitado: fora do escopo e mais dependências).

## 2. Validação cruzada temporal
- **Decisão**: `TimeSeriesSplit(n_splits=3, test_size=12, gap=GAP_MESES)` sobre as 72 linhas de treino.
- **Racional**: o `gap` impede que o alvo (12 meses à frente) das últimas linhas de treino de cada divisão caia dentro da validação.
- **Evidência (dados reais)**: treino de 24, 36 e 48 linhas; validação de 12 linhas com 50%, 100% e 100% de alta (ver `plan.md`).
- **Alternativas**: mais divisões (treinos ainda menores) ou validações menores (notas mais ruidosas); ambas rejeitadas por piorarem os dois problemas.

## 3. Nota da validação cruzada
- **Decisão (autor)**: juntar as previsões fora da amostra das 3 divisões e calcular um único macro-F1 e um único RMSE.
- **Racional**: macro-F1 por divisão é indefinido nas divisões com uma só classe.
- **Limitação**: 36 linhas agrupadas, só 6 de queda.
- **Alternativa rejeitada**: média por divisão (duas divisões degeneradas).

## 4. Desempate pelo modelo mais simples
- **Decisão (autor)**: dentro de uma tolerância da melhor nota, vence a configuração mais regularizada ou menos profunda; tolerâncias propostas de 0,03 (macro-F1, absoluta) e 3% (RMSE, relativa).
- **Racional**: com 72 linhas, diferenças pequenas são ruído; preferir simplicidade reduz sobreajuste.
- **Alternativa**: escolher sempre o máximo da nota (rejeitada: seleciona ruído).

## 5. Pipeline e padronização
- **Decisão**: `Pipeline([StandardScaler, modelo])` para os três modelos de cada tarefa.
- **Racional**: dentro de cada divisão, o scaler é ajustado só nos dados de treino da divisão, sem vazamento. Para o Random Forest a padronização é indiferente, mas mantém o código uniforme. Os coeficientes do modelo linear ficam em unidades padronizadas, comparáveis entre variáveis.

## 6. Modelos e grades
- Regressão logística: `C` em {0,01; 0,1; 1; 10}, penalidade L2, `max_iter` suficiente para convergir.
- Ridge: `alpha` em {0,1; 1; 10; 100; 1000} (1000 acrescentado em 2026-10-09; ver `plan.md`, decisão 7).
- Random Forest: `n_estimators = 300`, `max_depth` em {2, 3, 4}, `min_samples_leaf` em {5, 10}, `random_state = 42`.
- Peso das classes: `class_weight="balanced"` na logística e no Random Forest de classificação; não se aplica a Ridge nem ao Random Forest de regressão.
- Racional (decisão do autor): a métrica de decisão é macro-F1 e o treino tem 61% de alta; sem o peso, o modelo tende a prever quase sempre "alta". As métricas (macro-F1 e acurácia balanceada) continuam as mesmas.
- Seleção por macro-F1 (classificação) e RMSE (regressão).

## 7. Baselines
- Classificação: classe majoritária do treino (alta, 61%); persistência do sinal (alta se `acum12_passado > 0`).
- Regressão: média do alvo no treino; persistência (`acum12_passado` como previsão).
- Calculados com dados do treino, sem hiperparâmetros.

## 8. Métricas
- Classificação: macro-F1 (`labels=[0, 1]`, `zero_division=0`), acurácia balanceada, matriz de confusão.
- Regressão: RMSE e MAE.
- Fora: MAPE (o alvo cruza zero) e acurácia simples como métrica de decisão.

## 9. Armazenamento entre scripts
- **Decisão**: CSV para os dados de modelagem e `joblib` para os modelos treinados, em `dados/processados/`.
- **Racional**: o teste fica em arquivo próprio, lido só pelo `10`, e os modelos já treinados não precisam ser reajustados no teste. O `joblib` já vem com o scikit-learn.
- **Alternativa**: reajustar no `10` (rejeitada: duplicaria código e abriria brecha para ajustes com o teste à vista).

## 10. Importância das variáveis
- Modelo linear: coeficientes do modelo padronizado (logística e Ridge).
- Random Forest: `feature_importances_`. Com 72 linhas e variáveis correlacionadas, a importância é só indicativa.
