# scripts/test_connection.py

import os
from binance.client import Client
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

# Probar la conexión con el balance
try:
    account_info = client.get_account()
    print("✅ Conexión exitosa. Balance disponible:")
    for balance in account_info['balances']:
        asset = balance['asset']
        free = float(balance['free'])
        if free > 0:
            print(f"{asset}: {free}")
except Exception as e:
    print(f"❌ Error al conectar con Binance: {e}")
