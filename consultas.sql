-- 1. Série diária: temperatura mínima, máxima e chuva.
SELECT data, temperatura_minima_c, temperatura_maxima_c, precipitacao_mm
FROM clima_diario
ORDER BY data;

-- 2. Dias com maior precipitação (inclui dias sem chuva, se retornados como zero).
SELECT data, precipitacao_mm
FROM clima_diario
WHERE precipitacao_mm IS NOT NULL
ORDER BY precipitacao_mm DESC
LIMIT 10;

-- 3. KPIs do período: média das máximas, maior máxima e chuva acumulada.
SELECT
    ROUND(AVG(temperatura_maxima_c), 2) AS media_temperatura_maxima_c,
    ROUND(MAX(temperatura_maxima_c), 2) AS maior_temperatura_maxima_c,
    ROUND(SUM(precipitacao_mm), 2) AS precipitacao_acumulada_mm
FROM clima_diario;

-- 4. Contagem de dias com precipitação acima de zero.
SELECT COUNT(*) AS dias_com_chuva
FROM clima_diario
WHERE precipitacao_mm > 0;
