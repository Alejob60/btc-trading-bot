# scheduler.py

import schedule
import time
from main import main
from datetime import datetime

# Configuración del intervalo de ejecución (cada 15 minutos)
INTERVAL_MINUTES = 15

def job():
    print(f"\n🕐 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ejecutando ciclo del bot...")
    try:
        main()
    except Exception as e:
        print(f"⚠️ Error durante la ejecución del bot: {e}")

# Programar el trabajo recurrente
schedule.every(INTERVAL_MINUTES).minutes.do(job)

print(f"🚀 BOT AUTOMÁTICO INICIADO - Ejecutando cada {INTERVAL_MINUTES} minutos")

# Bucle principal
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Ejecución detenida manualmente.")
