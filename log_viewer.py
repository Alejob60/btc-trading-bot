# log_viewer.py

import os
from datetime import datetime

LOG_FILE = "logs/decision_log.log"


def mostrar_logs(ultimas=20):
    if not os.path.exists(LOG_FILE):
        print("❌ No se encontró el archivo de log de decisiones.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        lineas = file.readlines()

    total = len(lineas)
    print(f"📘 Mostrando las últimas {min(ultimas, total)} decisiones de {total} entradas:\n")
    for linea in lineas[-ultimas:]:
        print(f"📌 {linea.strip()}")


def buscar_por_tipo(tipo):
    if not os.path.exists(LOG_FILE):
        print("❌ No se encontró el archivo de log.")
        return

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        coincidencias = [l for l in file.readlines() if tipo.upper() in l.upper()]

    print(f"🔍 Se encontraron {len(coincidencias)} entradas para '{tipo}':\n")
    for l in coincidencias[-10:]:
        print(f"🔹 {l.strip()}")


if __name__ == "__main__":
    print("\n📊 VISOR DE DECISIONES DEL BOT")
    print("1. Mostrar últimas decisiones")
    print("2. Buscar por tipo de decisión (e.g., BUY, AI_Validated, HOLD)")
    opcion = input("Selecciona una opción (1/2): ").strip()

    if opcion == "1":
        mostrar_logs()
    elif opcion == "2":
        tipo = input("🔍 Ingresa palabra clave o tipo a buscar: ").strip()
        buscar_por_tipo(tipo)
    else:
        print("❌ Opción no válida.")
