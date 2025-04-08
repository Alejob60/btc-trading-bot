# app/interfaces/trading_bot_interface.py

from abc import ABC, abstractmethod
from app.domain.market_data import MarketData
from app.domain.trade_signal import TradeSignal
from app.domain.order import Order

class TradingBotInterface(ABC):

    @abstractmethod
    def analyze_market(self, data: MarketData) -> TradeSignal:
        """Analiza los datos del mercado y genera una señal de trading."""
        pass

    @abstractmethod
    def execute_trade(self, signal: TradeSignal) -> Order:
        """Ejecuta una orden basada en la señal de trading."""
        pass

    @abstractmethod
    def monitor_order(self, order: Order) -> Order:
        """Monitorea una orden abierta y actualiza su estado."""
        pass
