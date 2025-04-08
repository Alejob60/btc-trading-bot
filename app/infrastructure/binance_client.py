# app/infrastructure/binance_client.py

import os
from binance.client import Client
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_binance_client():
    if not API_KEY or not API_SECRET:
        raise ValueError("❌ Faltan las claves API en el archivo .env")

    client = Client(API_KEY, API_SECRET)
    
    # Verificación opcional
    try:
        status = client.get_system_status()
        if status["status"] == 0:
            print("✅ Conexión a Binance exitosa")
        else:
            print("⚠️ Binance reporta mantenimiento o problemas.")
    except Exception as e:
        print(f"❌ Error al conectar con Binance: {e}")
        raise e

    return client
