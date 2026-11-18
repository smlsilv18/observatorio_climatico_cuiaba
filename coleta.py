"""Coleta dados diários históricos da Open-Meteo e preserva o JSON original."""
from pathlib import Path
from datetime import date
import json
import requests

LATITUDE = -15.6014
LONGITUDE = -56.0979
INICIO = "2026-10-01"
FIM = "2026-10-30"
FUSO = "America/Cuiaba"
URL = "https://archive-api.open-meteo.com/v1/archive"
PASTA_DADOS = Path(__file__).resolve().parent / "dados"
ARQUIVO_JSON = PASTA_DADOS / "dados_originais.json"

def coletar():
    PASTA_DADOS.mkdir(exist_ok=True)
    parametros = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": INICIO,
        "end_date": FIM,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "temperature_unit": "celsius",
        "precipitation_unit": "mm",
        "timezone": FUSO,
    }
    resposta = requests.get(URL, params=parametros, timeout=60)
    resposta.raise_for_status()
    dados = resposta.json()
    if "daily" not in dados or "time" not in dados["daily"]:
        raise ValueError(f"Resposta inesperada da API: {dados}")
    # Preserva a resposta integral recebida, sem alterações.
    ARQUIVO_JSON.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"JSON original salvo em: {ARQUIVO_JSON}")
    print(f"Localidade: Cuiabá/MT | período: {INICIO} a {FIM}")
    print(f"Registros retornados: {len(dados['daily']['time'])}")
    print(f"Coleta realizada em: {date.today().isoformat()}")
    return dados

if __name__ == "__main__":
    coletar()
