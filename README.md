# Observatório Climático Local — Cuiabá/MT

## Objetivo
Organizar e analisar dados meteorológicos históricos de Cuiabá/MT para produzir informações iniciais sobre temperatura e precipitação, úteis à compreensão das condições climáticas locais.

## Público-alvo
Moradores, estudantes, trabalhadores e pessoas interessadas nas condições meteorológicas de Cuiabá.

## Recorte
- Localidade: Cuiabá/MT
- Coordenadas: latitude -15.6014; longitude -56.0979
- Período: 01/10/2026 a 30/10/2026 (30 dias)
- Variáveis: temperatura mínima diária (°C), temperatura máxima diária (°C) e precipitação diária acumulada (mm)
- Fonte: Open-Meteo Historical Weather API (`https://archive-api.open-meteo.com/v1/archive`)
- Fuso: `America/Cuiaba`

## Estrutura
- `coleta.py`: consulta a API e preserva a resposta integral em JSON.
- `banco.py`: tratamento, validação e carga idempotente no DuckDB.
- `consultas.sql`: consultas da análise.
- `dados/`: JSON original e banco DuckDB gerados durante a execução.
- `docs/escopo-1/AE2/`: relatório técnico.

## Preparação
Recomendado Python 3.10 ou superior.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução
Na raiz do repositório, execute na ordem:

```bash
python coleta.py
python banco.py
```

O arquivo `dados/dados_originais.json` preserva a resposta recebida da API. O arquivo `dados/observatorio.duckdb` contém a tabela `clima_diario`. Para executar as consultas, abra o banco no DuckDB e execute o conteúdo de `consultas.sql`.

## Tabela principal: clima_diario
- `data` DATE, chave primária: dia do registro.
- `temperatura_minima_c` DOUBLE: temperatura mínima diária em °C.
- `temperatura_maxima_c` DOUBLE: temperatura máxima diária em °C.
- `precipitacao_mm` DOUBLE: precipitação acumulada diária em mm.

## Perguntas e indicadores
1. Como variaram as temperaturas mínima e máxima em cada dia?
2. Quais dias tiveram maior precipitação?
3. Qual a média das temperaturas máximas e a precipitação acumulada no período?

KPIs: média das temperaturas máximas (°C), maior temperatura máxima (°C) e precipitação acumulada (mm).

## Qualidade e reexecução
O tratamento converte datas e números, verifica 30 dias, datas duplicadas, cobertura do período, coerência entre mínima e máxima e precipitação negativa. Valores ausentes são preservados como nulos, nunca convertidos automaticamente em zero. A carga apaga e recarrega somente o recorte definido, evitando duplicidade quando o processo é repetido.

## Limitações
Os dados da Open-Meteo são dados meteorológicos históricos modelados/reanalisados e não devem ser descritos como medições diretas de uma estação local sem confirmação. O recorte de 30 dias não representa todo o clima anual e não constitui previsão meteorológica. Resultados são descritivos e não demonstram, isoladamente, relações causais ou impactos na saúde. Não são coletados dados pessoais da comunidade.

## Reprodutibilidade
A coleta exige conexão com a internet. Registre no relatório a data efetiva da coleta, a quantidade retornada, as validações, os resultados reais dos KPIs e inclua capturas de tela da execução. Não invente resultados antes de executar os scripts.
