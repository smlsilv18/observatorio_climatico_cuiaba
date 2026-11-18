"""Trata, valida e carrega os dados diários no DuckDB."""
from pathlib import Path
import json
import pandas as pd
import duckdb

BASE = Path(__file__).resolve().parent
ARQUIVO_JSON = BASE / "dados" / "dados_originais.json"
ARQUIVO_BANCO = BASE / "dados" / "observatorio.duckdb"
INICIO = "2026-10-01"
FIM = "2026-10-30"

def preparar_dataframe():
    if not ARQUIVO_JSON.exists():
        raise FileNotFoundError("Execute primeiro: python coleta.py")
    bruto = json.loads(ARQUIVO_JSON.read_text(encoding="utf-8"))
    diario = bruto["daily"]
    df = pd.DataFrame({
        "data": diario["time"],
        "temperatura_minima_c": diario["temperature_2m_min"],
        "temperatura_maxima_c": diario["temperature_2m_max"],
        "precipitacao_mm": diario["precipitation_sum"],
    })
    df.columns = [c.strip().lower() for c in df.columns]
    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    for coluna in ["temperatura_minima_c", "temperatura_maxima_c", "precipitacao_mm"]:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    if df["data"].isna().any():
        raise ValueError("Há datas inválidas; carga cancelada.")
    if df["data"].duplicated().any():
        raise ValueError("Há datas duplicadas; carga cancelada.")
    if len(df) != 30:
        raise ValueError(f"Esperados 30 registros, recebidos {len(df)}.")
    if str(df["data"].min()) != INICIO or str(df["data"].max()) != FIM:
        raise ValueError("A cobertura de datas não corresponde ao período esperado.")
    if (df["temperatura_minima_c"] > df["temperatura_maxima_c"]).any():
        raise ValueError("Inconsistência: temperatura mínima maior que a máxima.")
    if (df["precipitacao_mm"].dropna() < 0).any():
        raise ValueError("Inconsistência: precipitação negativa.")

    ausentes = df.isna().sum()
    print("Resumo da validação:")
    print(f"Registros: {len(df)} | período: {df['data'].min()} a {df['data'].max()}")
    print(f"Duplicidades: {df['data'].duplicated().sum()}")
    print("Valores ausentes por coluna:")
    print(ausentes.to_string())
    # Ausências permanecem NULL/NaN; não são substituídas por zero.
    return df

def carregar():
    df = preparar_dataframe()
    ARQUIVO_BANCO.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(ARQUIVO_BANCO))
    try:
        con.execute("""
            CREATE TABLE IF NOT EXISTS clima_diario (
                data DATE PRIMARY KEY,
                temperatura_minima_c DOUBLE,
                temperatura_maxima_c DOUBLE,
                precipitacao_mm DOUBLE
            )
        """)
        con.register("df_temporario", df)
        # Reexecução idempotente: remove as datas do recorte antes de recarregá-las.
        con.execute("BEGIN TRANSACTION")
        con.execute("DELETE FROM clima_diario WHERE data BETWEEN ? AND ?", [INICIO, FIM])
        con.execute("""
            INSERT INTO clima_diario
            SELECT data, temperatura_minima_c, temperatura_maxima_c, precipitacao_mm
            FROM df_temporario
        """)
        con.execute("COMMIT")
        print("\\nAmostra da tabela carregada:")
        print(con.execute("SELECT * FROM clima_diario ORDER BY data LIMIT 5").df().to_string(index=False))
        print(f"\\nBanco salvo em: {ARQUIVO_BANCO}")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()

if __name__ == "__main__":
    carregar()
