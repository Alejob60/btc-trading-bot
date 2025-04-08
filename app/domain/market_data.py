# app/domain/market_data.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MarketData:
    symbol: str
    open_time: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    close_time: datetime

    def is_bullish(self) -> bool:
        return self.close_price > self.open_price

    def is_bearish(self) -> bool:
        return self.close_price < self.open_price
