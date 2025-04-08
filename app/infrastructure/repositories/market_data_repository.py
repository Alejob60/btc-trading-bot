from datetime import datetime, timedelta
from app.domain.market_data import MarketData

class MarketDataRepository:
    def get_latest_data(self) -> MarketData:
        now = datetime.now()
        return MarketData(
            symbol="BTCUSDT",
            open_time=now - timedelta(minutes=15),
            open_price=79200.0,
            high_price=79600.0,
            low_price=79000.0,
            close_price=79500.0,
            volume=2500.0,
            close_time=now
        )
