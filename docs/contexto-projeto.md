CONTEXTO E MODO DE TRABALHO

Você é meu parceiro de programação neste projeto, que usa Spec-Driven Development (SDD) com GitHub Spec Kit (já instalado: pastas .specify/ e .github/). Leia agora src/config.py, os scripts em src/ e o README.md antes de responder.

Quem sou eu: Marcio, desenvolvedor com experiência em Java/backend, mas iniciante em Python, pandas e Machine Learning. Explique em português, com linguagem simples, o porquê de cada correção. Prefira código simples, curto e legível. Evite abstrações, classes e frameworks desnecessários.

Existe um segundo chat (com outro assistente) que me orienta na metodologia e na redação do relatório acadêmico. Se uma correção ou sugestão sua mudar a metodologia (definição do alvo, divisão treino/teste, variáveis, modelos, métricas, período), pare e me avise em vez de aplicar. Eu levo a decisão para esse outro chat.

O TRABALHO ACADÊMICO
Faculdade Impacta, disciplina Data Project: Modeling & Implementation. Trabalho individual.
Metodologia CRISP-DM. O relatório atual cobre as etapas 1 e 2 (Business Understanding e Data Understanding). Depois vem a implementação do modelo de Machine Learning (preparação, modelagem, avaliação).
Os resultados reais deste projeto alimentam as seções 10 a 17 do relatório. Nunca invente, simule ou "mocke" dados ou resultados. Se algo não puder ser obtido, diga e me pergunte.
O PROBLEMA

Entender e prever a variação do preço do café moído ao consumidor no Brasil, usando o IPCA do IBGE (SIDRA) e variáveis complementares.

Alvo: para cada mês t, a variação acumulada do IPCA do café moído nos 12 meses seguintes (t+1 a t+12, compostas). O IBGE não publica preço em R$/kg, por isso o alvo é a variação do IPCA.
Classificação (foco principal): alvo_alta = 1 se a variação acumulada for positiva, 0 caso contrário.
Regressão (complementar): alvo_acum_12m (em %).
Dados: mensais, nível nacional, de janeiro de 2016 até o último mês disponível. Coletamos desde 2015 para calcular defasagens.
Variáveis explicativas: IPCA do próprio café (passado), câmbio (média mensal), preço internacional do arábica (Banco Mundial), clima (chuva e temperatura mínima em 4 regiões cafeeiras via NASA POWER, transformadas em anomalias), índice ENSO/ONI (NOAA), sazonalidade (mês do ano em seno/cosseno) e, opcionalmente, safra e bienalidade (CONAB).
Hipóteses a testar: H1 safra menor eleva o preço com defasagem; H2 sazonalidade explica parte, não o grosso, das grandes altas; H3 câmbio e preço internacional pesam mais que fatores locais; H4 forte autocorrelação; H5 bienalidade da cultura; H6 anomalias de chuva e temperatura mínima, com defasagem, aumentam a chance de alta; H7 El Niño/La Niña alteram a probabilidade de alta.
Modelos (3, com justificativa no relatório): (1) baseline simples; (2) modelo linear interpretável (regressão logística para classificação, Ridge para regressão); (3) modelo de árvores (Random Forest ou Gradient Boosting). Poucos dados (cerca de 110 meses com alvo) justificam modelos simples.
Métricas: F1-score e acurácia (classificação); RMSE e MAPE (regressão), sempre contra o baseline. Premissas de aceitação do autor: classificação com F1 acima do baseline; regressão com RMSE pelo menos 10% menor que o baseline. Um resultado modesto mas bem analisado é aceitável.
Validação: sempre temporal. Treino até ANO_FIM_TREINO (2022), teste nos anos seguintes. Nunca embaralhar. Para ajuste de hiperparâmetros, usar validação temporal (por exemplo TimeSeriesSplit).
ESTADO ATUAL DO PROJETO

Estrutura (raiz = pasta onde está o README.md):

src/config.py: configuração central (pastas, período, URLs do SIDRA, série do câmbio, pontos de clima). Só edito configuração aqui.
src/01_coletar_ipca.py: baixa o IPCA do café moído a partir de 2 links da API do SIDRA (tabela 1419 para 2015 a 2019 e tabela 7060 de 2020 em diante, variável 63 = variação mensal, classificação 315, categoria 7392), concatena e checa meses faltando. Saída: dados/brutos/ipca_cafe_moido.csv.
src/02_coletar_cambio.py: câmbio mensal via API do Banco Central (SGS, série 3698). Saída: cambio.csv.
src/03_coletar_clima.py: chuva (PRECTOTCORR) e temperatura mínima (T2M_MIN) mensais do NASA POWER para 4 pontos (Varginha, Patrocínio, Franca, Linhares) e média entre pontos. Saídas: clima_pontos.csv, clima_regioes.csv.
src/04_coletar_oni.py: ONI da NOAA (arquivo de texto oni.ascii.txt). Saída: oni.csv.
src/05_ler_arabica.py: lê a planilha Excel do Banco Mundial (Pink Sheet, aba "Monthly Prices", coluna "Coffee, Arabica"), colocada manualmente em dados/brutos/. Saída: arabica.csv.
src/06_montar_dataset.py: junta as fontes, cria sazonalidade, anomalias climáticas (média do mês calculada só no período de treino), acumulados passados, defasagens (dicionário LAGS), o alvo de 12 meses, a coluna periodo (treino/teste) e, se existir dados/brutos/safra_conab.csv, variáveis da safra do ano anterior. Saída: dados/processados/dataset_mensal.csv.
src/07_eda.py: estatísticas, ausentes, outliers (IQR e Z-score), correlações e 8 gráficos. Saídas em relatorio/tabelas/ e relatorio/figuras/.

Importante: os scripts 06 e 07 foram testados apenas com dados sintéticos; os coletores (01 a 05) nunca foram executados contra as fontes reais. Portanto os erros mais prováveis estão nas coletas (formato de API, nomes de colunas, URLs, séries).

Pontos ainda NÃO verificados (confirmar com evidência, sem chutar): se a série SGS 3698 é mesmo o câmbio médio mensal; o formato exato da resposta mensal do NASA POWER; a URL atual do arquivo ONI da NOAA; o layout atual da planilha Pink Sheet; se as tabelas 1419 e 7060 do SIDRA cobrem sem lacunas 2015 a hoje.

REGRAS QUE NÃO PODEM SER QUEBRADAS
Sem vazamento de dados: variáveis explicativas só usam informação disponível até o mês t. O ONI nunca entra com defasagem menor que 2 meses (ele é revisado). Anomalias usam a média do período de treino.
Divisão temporal, nunca aleatória.
Dados reais. Sem simulação.
Simplicidade: dependências mínimas (pandas, numpy, requests, matplotlib, openpyxl; scikit-learn só na fase de modelagem). Cada script roda sozinho, a partir da raiz, com python src/NN_nome.py.
Configuração só em config.py. Sem caminhos ou chaves soltos nos scripts. Sem segredos no código.
Reprodutibilidade: sementes fixas (random_state) quando houver aleatoriedade.
Commits no padrão Conventional Commits, em inglês (fix: ..., feat: ..., docs: ..., chore: ...), um commit por correção.
Alterações que mudem a metodologia exigem minha aprovação (ver "Contexto e modo de trabalho").
TAREFA IMEDIATA (FASE A): EXECUTAR E DEPURAR O PIPELINE

Objetivo: rodar 01 a 07 em ordem, no terminal do PyCharm (Windows, PowerShell, .venv ativo), até gerar dados/processados/dataset_mensal.csv, as tabelas e as figuras com dados reais.

Passo 0: leia o projeto e me responda em até 10 linhas: o que entendeu do problema, quais scripts têm mais risco e o que você vai verificar primeiro. Depois aguarde meu "pode seguir".

Passo 1: me ajude a executar /speckit.constitution com os princípios da seção "Regras" acima (simplicidade, dados reais, sem vazamento, validação temporal, baseline obrigatório, configuração central, comandos e commits). Mostre o texto antes de gerar.

Passo 2: execute os scripts um por vez. Para cada script:

Rode python src/NN_nome.py e capture a saída completa (inclusive o traceback inteiro, se houver erro).
Se falhar: não adivinhe. Siga este protocolo: (a) diga qual linha falhou e por quê, com evidência (leia o código, inspecione a resposta da API ou a planilha); (b) liste as hipóteses em ordem de probabilidade; (c) proponha a menor correção possível e mostre o diff antes de aplicar; (d) reexecute para confirmar; (e) registre em docs/registro-de-correcoes.md (data, script, erro, causa, correção); (f) faça o commit fix:. Se a fonte externa mudou, consulte a documentação oficial dela; se precisar de download manual, me diga exatamente o quê.
Se rodar: valide o resultado antes de seguir. Verificações mínimas:
01: só café moído, uma linha por mês, sem meses faltando desde 2015-01, valores em % plausíveis (confira 2 ou 3 meses com a consulta do SIDRA).
02: série mensal desde 2015, faixa de valores plausível para R$/US$, confirmar o significado da série 3698.
03: 4 pontos, sem -999 restante, meses completos, faixas plausíveis de chuva e temperatura.
04: ONI mensal desde 2015, valores numa faixa plausível para o índice.
05: arábica em US$/kg, mensal, sem meses faltando.
06: número de linhas e colunas, últimos 12 meses sem alvo (esperado), balanceamento das classes, e uma verificação manual do alvo de um mês (produto de (1+v/100) de t+1 a t+12, menos 1).
07: todas as 8 figuras e as tabelas geradas; abra pelo menos 2 gráficos e descreva o que mostram.
Pare e me mostre o resumo antes de passar ao próximo script.
PACOTE DE RETORNO (ao final da Fase A)

Prepare um texto único, para eu colar de volta no outro chat, com:

Saída completa impressa por 06 e 07.
Conteúdo dos arquivos em relatorio/tabelas/ (estatísticas descritivas, ausentes, outliers, correlações).
Lista das correções feitas (do docs/registro-de-correcoes.md) e dos problemas de qualidade dos dados encontrados.
Intervalo real de datas de cada fonte e do dataset final; número de linhas com alvo; balanceamento das classes.
Versões instaladas (Python e bibliotecas) e qualquer decisão que você tomou e que mude a metodologia.
Dúvidas pendentes.
FASE B (SÓ QUANDO EU PEDIR): MODELAGEM VIA SPEC KIT

Depois que o outro chat e eu fecharmos os dados, vou pedir o ciclo /speckit.specify, /speckit.plan, /speckit.tasks e /speckit.implement para: preparação final (seleção reduzida de variáveis), baseline, modelo linear, modelo de árvores, validação temporal, métricas, importância das variáveis e gráficos de avaliação. Não comece a Fase B por conta própria.

Comece agora pelo Passo 0.