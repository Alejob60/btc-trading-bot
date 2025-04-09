# app/services/position_manager.py

from app.domain.order import Order, OrderStatus
from app.infrastructure.market_data_provider import MarketDataProvider
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository
import time

class PositionManager:
    def __init__(self):
        self.market_provider = MarketDataProvider()
        self.logger = DecisionLogRepository()

    def evaluate_position(self, order: Order, signal_confidence: float) -> str:
        """
        Evalúa si una orden debe ser:
        - AMPLIFIED: aumentar posición si va bien
        - REDUCED: reducir si hay dudas
        - CLOSED: cerrar si hay riesgo
        - HOLD: mantener
        """
        try:
            current_price = self.market_provider.get_current_price(order.symbol)
            distance_from_entry = abs(current_price - order.entry_price)
            direction = 1 if order.order_type.name == "BUY" else -1
            gain = direction * (current_price - order.entry_price)

            if gain > 0 and signal_confidence >= 0.9:
                self.logger.log_decision(
                    symbol=order.symbol,
                    decision_type="Amplify_Position",
                    signal=order.order_type.name,
                    confidence=signal_confidence,
                    reason=f"Ganancia actual: {gain:.2f} | Condición positiva",
                    validated_by="PositionManager"
                )
                return "AMPLIFY"

            elif gain < 0 and signal_confidence < 0.7:
                self.logger.log_decision(
                    symbol=order.symbol,
                    decision_type="Reduce_Position",
                    signal=order.order_type.name,
                    confidence=signal_confidence,
                    reason=f"Pérdida detectada: {gain:.2f} | Confianza baja",
                    validated_by="PositionManager"
                )
                return "REDUCE"

            elif gain < -150:
                self.logger.log_decision(
                    symbol=order.symbol,
                    decision_type="Close_Position",
                    signal=order.order_type.name,
                    confidence=signal_confidence,
                    reason=f"Pérdida severa: {gain:.2f}",
                    validated_by="PositionManager"
                )
                return "CLOSE"

            return "HOLD"

        except Exception as e:
            print(f"⚠️ Error en PositionManager: {e}")
            return "HOLD"
