# Registro de correções

| Data | Script | Erro | Causa | Correção |
|---|---|---|---|---|
| 2026-10-09 | 01_coletar_ipca.py | `TimeoutError` na tabela 7060 (120 s) | Lentidão passageira do servidor SIDRA; `curl` respondeu em 0,3 s e a nova execução funcionou | Nenhuma alteração de código |
| 2026-10-09 | config.py / README.md (02) | Comentário dizia "PTAX venda", sem evidência | Série 3698 não é a PTAX: coincide com a média mensal do dólar comercial venda (SGS 1), verificado na API do BCB. Página de metadados do BCB inacessível | Comentário e README corrigidos para descrever a verificação real |
| 2026-10-09 | 03_coletar_clima.py | Sem erro; clima termina em 2026-08 | NASA POWER devolve -999 (sem dado) para 2026-09 e o script descarta o mês | Nenhuma alteração de código; limitação da fonte registrada |
| 2026-10-09 | config.py (09) | Melhor `alpha` do Ridge na borda da grade (100, RMSE 31,50; `alpha`=10 deu 32,54) | A grade {100, 10, 1, 0.1} parava em 100: melhor valor na borda sugere que um valor mais regularizado poderia ser melhor. Conferência feita só com o treino (teste fechado) | Acrescentado `alpha = 1000` (grade {1000, 100, 10, 1, 0.1}). Resultado: 1000 deu RMSE 32,58 (pior); a escolha continua `alpha = 100`, agora no interior da grade, sem efeito na escolha. Regra fixa: grade não será estendida de novo |
