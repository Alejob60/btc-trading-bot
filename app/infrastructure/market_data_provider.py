# app/infrastructure/market_data_provider.py

from binance.client import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from app.domain.market_data import MarketData

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
