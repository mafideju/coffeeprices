"""Previsão ILUSTRATIVA para 2026-09 (alvo ainda não existe), com os modelos já escolhidos só no treino."""
import sys

import joblib
import pandas as pd

import config

MES = pd.Timestamp("2026-09-01")


def main():
    df = pd.read_csv(config.DADOS_PROCESSADOS / "dataset_mensal.csv", parse_dates=["mes"])
    linha = df[df["mes"] == MES]
    if len(linha) != 1:
        print(f"ERRO: mês {MES:%Y-%m} não encontrado no dataset")
        sys.exit(1)
    if linha["alvo_acum_12m"].notna().any():
        print("ERRO: o alvo de 2026-09 já existe; a previsão não seria mais ilustrativa")
        sys.exit(1)
    X = linha[config.FEATURES_MODELO]
    if X.isna().any().any():
        print(f"ERRO: variáveis ausentes em {MES:%Y-%m}: {X.columns[X.isna().any()].tolist()}")
        sys.exit(1)

    salvo = joblib.load(config.DADOS_PROCESSADOS / "modelos_treinados.joblib")
    pipes, base = salvo["pipelines"], salvo["baselines"]
    acum = float(linha["acum12_passado"].iloc[0])
    previsoes = [
        ("classificacao", "baseline_maioria", base["classe_majoritaria"]),
        ("classificacao", "baseline_persistencia_sinal", int(acum > 0)),
        ("classificacao", "logistica", int(pipes["logistica"].predict(X)[0])),
        ("classificacao", "rf_classificacao", int(pipes["rf_classificacao"].predict(X)[0])),
        ("regressao", "baseline_media", base["media_alvo"]),
        ("regressao", "baseline_persistencia", acum),
        ("regressao", "ridge", float(pipes["ridge"].predict(X)[0])),
        ("regressao", "rf_regressao", float(pipes["rf_regressao"].predict(X)[0])),
    ]
    tabela = pd.DataFrame(previsoes, columns=["tarefa", "modelo", "previsao"])
    tabela.insert(0, "mes", f"{MES:%Y-%m}")
    tabela["janela_prevista"] = "2026-10 a 2027-09"
    tabela["rotulo"] = "ilustrativa"
    tabela.to_csv(config.TABELAS / "previsao_ilustrativa_2026-09.csv", index=False)

    print("PREVISÃO ILUSTRATIVA para 2026-09 (janela 2026-10 a 2027-09; não há valor real para comparar).")
    print("Os modelos têm desempenho modesto no teste (macro-F1 0,50 e 0,52; regressão sem superar a média).")
    print("Classificação: 1 = alta, 0 = queda. Regressão: variação acumulada em %.\n")
    print(tabela[["tarefa", "modelo", "previsao"]].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
