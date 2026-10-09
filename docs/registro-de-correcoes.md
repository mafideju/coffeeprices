# Registro de correções

| Data | Script | Erro | Causa | Correção |
|---|---|---|---|---|
| 2026-10-09 | 01_coletar_ipca.py | `TimeoutError` na tabela 7060 (120 s) | Lentidão passageira do servidor SIDRA; `curl` respondeu em 0,3 s e a nova execução funcionou | Nenhuma alteração de código |
| 2026-10-09 | config.py / README.md (02) | Comentário dizia "PTAX venda", sem evidência | Série 3698 não é a PTAX: coincide com a média mensal do dólar comercial venda (SGS 1), verificado na API do BCB. Página de metadados do BCB inacessível | Comentário e README corrigidos para descrever a verificação real |
