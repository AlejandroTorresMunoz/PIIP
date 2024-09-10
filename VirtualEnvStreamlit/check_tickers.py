"""
Script para poder comprobar la existencia de las empresas guardadas en el entorno de Yahoo Finance
"""

import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed

# Leer el archivo Excel
df = pd.read_excel("./data/CheckValoresBolsasMundiales.xlsx")
df['Is_In_TF'] = False

def check_ticker_exists(ticker):
    """
    Función para comprobar si un ticker existe en Yahoo Finance.
    """
    ticker = str(ticker)
    stock = yf.Ticker(ticker)
    try:
        _ = stock.info  # Intenta acceder a la información del ticker
        return ticker, True
    except:
        return ticker, False

# Usar ThreadPoolExecutor para paralelizar las consultas
try:
    with ThreadPoolExecutor(max_workers=5) as executor:  # Ajusta el número de workers según el rendimiento de tu máquina
        futures = {executor.submit(check_ticker_exists, row['Ticker']): index for index, row in df.iterrows()}

        for future in as_completed(futures):
            index = futures[future]
            ticker, exists = future.result()
            df.loc[index, 'Is_In_TF'] = exists
            # print(f"Consultado {ticker}: {'Existe' if exists else 'No existe'}")

except KeyboardInterrupt:
    print("\nEjecución interrumpida por el usuario. Guardando progreso y cerrando...")

df.to_csv("./data/CheckValoresBolsasMundiales.csv")