# 🤖 BTC Trading Bot (Clean Architecture)

Bot de trading algorítmico para Bitcoin (BTC/USDT), desarrollado en Python con una arquitectura limpia y modular. Este bot analiza datos de mercado en tiempo real, genera señales y ejecuta órdenes automáticas en Binance Futures.

## 🚀 Objetivos
- 📊 Monitoreo técnico continuo (RSI, StochRSI, MA, Bollinger)
- 🧠 Análisis con Inteligencia Artificial (IA)
- 🧪 Entradas inteligentes con control de riesgo y gestión del capital
- 🧵 Soporte para multihilos y monitoreo constante de órdenes
- 🧩 Arquitectura escalable con posibilidad de integrarse a un frontend

## 🏗️ Arquitectura (Clean Architecture)


## ⚙️ Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Alejob60/btc-trading-bot.git
cd btc-trading-bot

# Crear entorno virtual
python -m venv env
source env/bin/activate      # Linux/macOS
env\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar script de prueba de conexión
python scripts/test_connection.py

# Correr el bot (ejemplo básico)
python main.py


btc_bot/ │ ├── ai_engine/ # Lógica de IA y decisiones inteligentes 
├── app/ # Módulo principal del bot │ 
├    ├── domain/ # Entidades del dominio (Order, MarketData, etc.) │ 
├    ├── infrastructure/ # Acceso a datos externos (Binance, DB, etc.) │ 
├    ├── interfaces/ # Entradas/salidas (controladores) │ 
├    └── services/ # Lógica de negocio y flujos 
├   
├── scripts/ # Scripts utilitarios y pruebas 
├── config/ # Configuración y entorno 
├── .env # Variables de entorno (no subir al repo público) 
├── requirements.txt # Dependencias del proyecto 
└── main.py # Punto de entrada del bot

