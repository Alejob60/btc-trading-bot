# tools/decision_report.py

import os
from collections import Counter

LOG_FILE = "logs/decision_log.log"

def generar_reporte():
    if not os.path.exists(LOG_FILE):
        print("❌ No se encontró el archivo de log de decisiones.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    total = len(lineas)
    tipos = Counter()
    señales = Counter()
    validaciones = Counter()

    for linea in lineas:
        if "decision_type=" in linea:
            tipo = linea.split("decision_type=")[1].split(",")[0].strip()
            tipos[tipo] += 1
        if "signal=" in linea:
            señal = linea.split("signal=")[1].split(",")[0].strip()
            señales[señal] += 1
        if "validated_by=" in linea:
            val = linea.split("validated_by=")[1].strip()
            validaciones[val] += 1

    print("\n📊 RESUMEN DE DECISIONES DEL BOT")
    print(f"Total de decisiones registradas: {total}\n")

    print("🔹 Tipos de decisión:")
    for tipo, count in tipos.items():
        print(f"  - {tipo}: {count}")

    print("\n🔹 Señales generadas:")
    for sig, count in señales.items():
        print(f"  - {sig}: {count}")

    print("\n🔹 Validado por:")
    for val, count in validaciones.items():
        print(f"  - {val}: {count}")


def log_order(order, source="unknown"):
    from datetime import datetime
    path = "logs/decision_log.log"
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(path, "a", encoding="utf-8") as log:
        log.write(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] decision_type=Order_Executed, symbol={order.symbol}, action={order.side}, price={order.entry_price}, tp={order.take_profit}, sl={order.stop_loss}, source={source}\n"
        )


if __name__ == "__main__":
    generar_reporte()
