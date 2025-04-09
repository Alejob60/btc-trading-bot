# app/infrastructure/market_data_provider.py

from binance.client import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from app.domain.market_data import MarketData
import requests
load_dotenv()

class MarketDataProvider:
    def __init__(self):
        self.client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))

    def get_latest_market_data(self, symbol: str = "BTCUSDT", interval: str = Client.KLINE_INTERVAL_15MINUTE) -> MarketData:
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=1)
        k = klines[0]

        return MarketData(
            symbol=symbol,
            open_time=datetime.fromtimestamp(k[0] / 1000.0),
            open_price=float(k[1]),
            high_price=float(k[2]),
            low_price=float(k[3]),
            close_price=float(k[4]),
            volume=float(k[5]),
            close_time=datetime.fromtimestamp(k[6] / 1000.0)
        )
    def get_recent_candles(self, symbol="BTCUSDT", limit=20, interval="15m"):
        try:
            raw_data = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            candles = []
            for entry in raw_data:
                candles.append({
                    "open": float(entry[1]),
                    "high": float(entry[2]),
                    "low": float(entry[3]),
                    "close": float(entry[4])
                })
            return candles
        except Exception as e:
            print(f"⚠️ Error al obtener velas recientes: {e}")
            return []
    def get_current_price(self, symbol: str) -> float:
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            response = requests.get(url)
            response.raise_for_status()
            return float(response.json()['price'])
        except Exception as e:
            print(f"❌ Error al obtener el precio actual de {symbol}: {e}")
            return 0.0