# app/services/order_monitor.py
from datetime import datetime
from app.domain.order import OrderStatus
from app.infrastructure.market_data_provider import MarketDataProvider
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository


class OrderMonitor:

    def __init__(self):
        self.market_data_provider = MarketDataProvider()
        self.logger = DecisionLogRepository()

    def monitor(self, order):
        if order.status != OrderStatus.OPEN:
            return

        print(f"🕒 Monitoreando orden: {order.order_type.name} {order.symbol}")

        current_price = self.market_data_provider.get_current_price(order.symbol)
        print(f"📡 Precio actual: {current_price} | TP: {order.take_profit} | SL: {order.stop_loss}")

        # Lógica de monitoreo
        if order.order_type.name == "BUY":
            if current_price >= order.take_profit:
                print("🎯 ¡Take Profit alcanzado (compra)! Cerrando orden.")
                order.status = OrderStatus.CLOSED
            elif current_price <= order.stop_loss:
                print("🛑 ¡Stop Loss alcanzado (compra)! Cerrando orden.")
                order.status = OrderStatus.CLOSED

        elif order.order_type.name == "SELL":
            if current_price <= order.take_profit:
                print("🎯 ¡Take Profit alcanzado (venta)! Cerrando orden.")
                order.status = OrderStatus.CLOSED
            elif current_price >= order.stop_loss:
                print("🛑 ¡Stop Loss alcanzado (venta)! Cerrando orden.")
                order.status = OrderStatus.CLOSED

        # Si se cerró, loguear
        if order.status == OrderStatus.CLOSED:
            order.closed_at = datetime.now()
            print(f"✅ Orden cerrada. Esperando próximo análisis.")
            self.logger.log_decision(
                symbol=order.symbol,
                decision_type="Order_Closed",
                signal=order.order_type.name,
                confidence=0.0,
                reason="TP/SL alcanzado",
                validated_by="OrderMonitor"
            )
