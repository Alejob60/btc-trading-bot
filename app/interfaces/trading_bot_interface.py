from abc import ABC, abstractmethod
from app.domain.market_data import MarketData
from app.domain.tradeSignal import TradeSignal
from app.domain.order import Order


class TradingBotInterface(ABC):

    @abstractmethod
    def analyze_market(self, data: MarketData) -> TradeSignal:
        """Analiza los datos del mercado y genera una señal de trading"""
        pass

    @abstractmethod
    def execute_trade(self, signal: TradeSignal) -> Order:
        """Ejecuta una orden según la señal generada"""
        pass
