# app/services/trading_bot_service.py
from app.interfaces.trading_bot_interface import TradingBotInterface
from app.domain.market_data import MarketData
from app.domain.tradeSignal import TradeSignal, SignalType
from app.domain.order import Order, OrderType, OrderStatus
from datetime import datetime
import os
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository

class TradingBotService(TradingBotInterface):

    def __init__(self):
        self.log_repo = DecisionLogRepository(log_path="logs/decision_log.log")

    def analyze_market(self, data: MarketData) -> TradeSignal:
        if data.is_bullish():
            signal = SignalType.BUY
            confidence = 0.9
            reason = "Velas verdes consecutivas y volumen en aumento"
        elif data.is_bearish():
            signal = SignalType.SELL
            confidence = 0.9
            reason = "Velas rojas consecutivas y caída de volumen"
        else:
            signal = SignalType.HOLD
            confidence = 0.5
            reason = "Tendencia lateral"

        trade_signal = TradeSignal(
            symbol=data.symbol,
            signal_type=signal,
            confidence=confidence,
            reason=reason,
            generated_at=datetime.now()
        )

        # Registrar señal en log
        self.log_repo.log_signal(trade_signal, source="analyze_market")

        return trade_signal

    def execute_trade(self, signal: TradeSignal) -> Order:
        amount = 0.001  # valor fijo por ahora
        entry_price = 79300.0  # simulado, en producción lo obtienes en tiempo real
        take_profit = entry_price * 1.02
        stop_loss = entry_price * 0.98

        order = Order(
            symbol=signal.symbol,
            order_type=OrderType.BUY if signal.signal_type == SignalType.BUY else OrderType.SELL,
            amount=amount,
            entry_price=entry_price,
            take_profit=take_profit,
            stop_loss=stop_loss,
            status=OrderStatus.OPEN,
            opened_at=datetime.now()
        )

        # Registrar orden en log
        self.log_repo.log_order(order, source="execute_trade")

        return order
