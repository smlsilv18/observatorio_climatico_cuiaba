# Relatório técnico e analítico — AE2
## Observatório Climático Local: Cuiabá/MT

### 1. Contextualização e continuidade da AE1
O projeto Observatório Climático Local busca organizar informações meteorológicas para apoiar a compreensão das condições climáticas de Cuiabá/MT. A variação da temperatura e da precipitação pode influenciar o conforto térmico, o planejamento de atividades cotidianas e a percepção de períodos mais quentes ou chuvosos. O público beneficiário inclui moradores, estudantes e trabalhadores da cidade.

Como o planejamento/documento da AE1 não está disponível para consulta, este recorte foi reconstruído para dar continuidade ao tema do projeto. A alteração deve ser registrada como reorganização metodológica, e não como resultado de uma decisão documentada na AE1.

Localidade: Cuiabá/MT (latitude -15.6014; longitude -56.0979). Período: 01/10/2026 a 30/10/2026, totalizando 30 dias consecutivos. Variáveis: temperatura mínima diária (°C), temperatura máxima diária (°C) e precipitação acumulada diária (mm).

Perguntas analíticas:
1. Como variaram as temperaturas mínima e máxima em cada dia?
2. Quais dias apresentaram maior precipitação?
3. Qual foi a média das temperaturas máximas e o total de precipitação no período?

KPIs: (a) média das temperaturas máximas, em °C; (b) maior temperatura máxima diária, em °C; (c) precipitação acumulada, em mm.

### 2. Fonte e coleta
A fonte utilizada é a API histórica da Open-Meteo (`https://archive-api.open-meteo.com/v1/archive`). A coleta é realizada pelo script `coleta.py`, com Python e biblioteca Requests. Os parâmetros são latitude -15.6014, longitude -56.0979, início 2026-10-01, fim 2026-10-30, variáveis `temperature_2m_min`, `temperature_2m_max` e `precipitation_sum`, unidades Celsius e milímetros e fuso `America/Cuiaba`.

Data efetiva da coleta: **[PREENCHER após executar coleta.py]**. Quantidade retornada: **[PREENCHER]**. A resposta integral é preservada em `dados/dados_originais.json`, permitindo rastreabilidade. A base tratada é gravada em `dados/observatorio.duckdb`.

### 3. Tratamento e qualidade dos dados
O script `banco.py` utiliza pandas para organizar as séries diárias em uma tabela, padronizar os nomes das colunas em minúsculas e snake_case, converter datas para tipo de data e variáveis meteorológicas para valores numéricos. São verificadas datas inválidas, duplicidades, quantidade esperada de 30 registros, cobertura exata do período, temperaturas mínimas superiores às máximas e precipitação negativa.

Valores ausentes são convertidos em nulos e preservados; não são substituídos por zero, pois ausência de informação não significa ausência de chuva ou temperatura igual a zero. Após executar o script, registrar aqui os resultados reais da validação: **[PREENCHER ausentes, duplicidades, inconsistências e quantidade final]**.

### 4. Armazenamento e análise inicial
A tabela principal `clima_diario` possui: `data` (DATE, chave primária), `temperatura_minima_c` (DOUBLE), `temperatura_maxima_c` (DOUBLE) e `precipitacao_mm` (DOUBLE). O DuckDB é alimentado a partir do DataFrame validado. A rotina remove os registros do recorte antes de inserir os dados atualizados, tornando a execução repetida idempotente.

As consultas SQL respondem às perguntas analíticas: série diária ordenada por data; dez dias de maior precipitação; e cálculo dos três KPIs. Resultados reais após executar os scripts:
- Média das temperaturas máximas: **[PREENCHER] °C**. Cálculo: AVG(temperatura_maxima_c).
- Maior temperatura máxima: **[PREENCHER] °C**. Cálculo: MAX(temperatura_maxima_c).
- Precipitação acumulada: **[PREENCHER] mm**. Cálculo: SUM(precipitacao_mm).

Interpretação: **[DESCREVER com base nos resultados efetivamente obtidos, indicando os dias mais quentes e chuvosos]**. Evidências a inserir: captura da execução de `coleta.py`, amostra da tabela `clima_diario` e resultados das consultas SQL, com legendas e explicações.

Critérios de sucesso preliminares: a coleta será considerada tecnicamente concluída se retornar os 30 dias esperados; a qualidade será avaliada pela ausência de duplicidades e inconsistências ou pelo registro justificado de problemas; o armazenamento será validado pela existência da tabela e pela reexecução sem duplicar datas. A utilidade para o público e a compreensão dos resultados dependem de avaliação e devolutiva em etapas posteriores.

### 5. Relevância extensionista, ética e limitações
Os indicadores podem ajudar moradores e estudantes a reconhecer a variação recente de temperatura e chuva e apoiar conversas informadas sobre cuidados em dias quentes e planejamento de atividades. Não substituem alertas oficiais nem orientações de saúde ou defesa civil.

A análise cobre apenas 30 dias de outubro de 2026, portanto não permite caracterizar o clima de todo o ano nem estabelecer tendências climáticas de longo prazo. A Open-Meteo fornece dados históricos baseados em modelos/reanálises; os valores não devem ser apresentados como medições diretas de uma estação meteorológica específica de Cuiabá sem confirmação. Trata-se de análise histórica descritiva, não de previsão do tempo.

O projeto utiliza somente variáveis meteorológicas agregadas, sem identificação de moradores. Caso sejam coletados relatos da comunidade em etapas futuras, deverão ser solicitados apenas os dados necessários, com informação clara sobre finalidade, consentimento, acesso restrito e anonimização sempre que possível.
