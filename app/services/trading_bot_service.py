from app.interfaces.trading_bot_interface import TradingBotInterface
from app.domain.market_data import MarketData
from app.domain.tradeSignal import TradeSignal, SignalType
from app.domain.order import Order, OrderType, OrderStatus
from datetime import datetime
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository
from app.infrastructure.market_data_provider import MarketDataProvider

class TradingBotService(TradingBotInterface):
    def __init__(self):
        self.log_repo = DecisionLogRepository()
        self.market_data_provider = MarketDataProvider()

    def analyze_market(self, data: MarketData) -> TradeSignal:
        if data.is_bullish():
            signal = SignalType.BUY
            confidence = 0.9
            reason = "Velas verdes consecutivas con volumen en aumento"
        elif data.is_bearish():
            signal = SignalType.SELL
            confidence = 0.9
            reason = "Velas rojas consecutivas con volumen decreciente"
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

        self.log_repo.log_decision(
            symbol=trade_signal.symbol,
            decision_type="Technical",
            signal=trade_signal.signal_type.name,
            confidence=trade_signal.confidence,
            reason=trade_signal.reason,
            validated_by="analyze_market"
        )
        return trade_signal

    def execute_trade(self, signal: TradeSignal, entry_price: float) -> Order:
        amount = 0.001

        if signal.signal_type == SignalType.BUY:
            take_profit = entry_price * 1.02  # Ganamos si sube
            stop_loss = entry_price * 0.98    # Perdemos si baja
        else:  # SELL
            take_profit = entry_price * 0.98  # Ganamos si baja
            stop_loss = entry_price * 1.02    # Perdemos si sube

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

        self.log_repo.log_order(order, source="execute_trade")
        return order

