# main.py

from app.infrastructure.market_data_provider import MarketDataProvider
from app.infrastructure.repositories.trade_signal_repository import TradeSignalRepository
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository
from app.services.trading_bot_service import TradingBotService
from app.services.order_monitor import OrderMonitor
from ai_engine.decision_engine import DecisionEngine
from app.services.predictive_model_service import PredictiveModelService
import time


def main():
    print("\U0001F680 Bot de trading para BTC/USDT ejecutándose en MODO CONSERVADOR...")

    # Inicialización de servicios
    market_data_provider = MarketDataProvider()
    trade_signal_repo = TradeSignalRepository()
    bot_service = TradingBotService()
    order_monitor = OrderMonitor()
    decision_engine = DecisionEngine()
    decision_log = DecisionLogRepository()
    predictive_model = PredictiveModelService()

    active_order = None

    while True:
        try:
            # Precio en tiempo real (para entrada de órdenes y monitoreo)
            current_price = market_data_provider.get_current_price("BTCUSDT")
            print(f"\U0001F4CA Precio actual: {current_price}")

            # 1. Obtener velas de múltiples marcos de tiempo
            candles_1h = market_data_provider.get_recent_candles(symbol="BTCUSDT", limit=20, interval="1h")
            candles_15m = market_data_provider.get_recent_candles(symbol="BTCUSDT", limit=20, interval="15m")

            # 2. Análisis multiframe (macro + corto plazo)
            prediction = predictive_model.analyze_multiframe(candles_1h, candles_15m)
            print(f"\U0001F9E0 Predicción IA: {prediction}")

            # 3. Datos de mercado actuales (última vela)
            market_data = market_data_provider.get_latest_market_data()

            # 4. Señal técnica con lógica propia
            signal = bot_service.analyze_market(market_data)
            print(f"\U0001F4C8 Señal técnica: {signal.signal_type.name}, confianza: {signal.confidence}")

            # 5. Comparar decisiones: si coinciden, ejecutamos
            if prediction["decision"] == signal.signal_type.name:
                trade_signal_repo.save(signal)
                decision_log.log_decision(
                    symbol=signal.symbol,
                    decision_type="Validated",
                    signal=signal.signal_type.name,
                    confidence=signal.confidence,
                    reason=prediction["reason"],
                    validated_by="Multiframe + Técnica"
                )

                if active_order is None:
                    order = bot_service.execute_trade(signal, current_price)
                    active_order = order
                    print(f"\U0001F4E4 Orden ejecutada: {order.order_type.name} @ {order.entry_price}")

                    # Monitorear orden activamente
                    while active_order and active_order.status == order.status:
                        result = order_monitor.monitor_order(active_order)
                        if result:
                            decision_log.log_decision(
                                symbol=active_order.symbol,
                                decision_type="Order_Closed",
                                signal=active_order.order_type.name,
                                confidence=signal.confidence,
                                reason="Orden cerrada por TP o SL",
                                validated_by="Monitor"
                            )
                            print("✅ Orden cerrada. Esperando próximo análisis.")
                            active_order = None
                        time.sleep(15)

            else:
                print("⏸️ Señales no coinciden, reevaluando con IA...")
                if decision_engine.revalidate_with_context(signal, candles_1h + candles_15m):
                    decision_log.log_decision(
                        symbol=signal.symbol,
                        decision_type="Revalidated",
                        signal=signal.signal_type.name,
                        confidence=signal.confidence,
                        reason="Revalidación positiva IA",
                        validated_by="GPT/DeepSeek"
                    )
                    if active_order is None:
                        order = bot_service.execute_trade(signal, current_price)
                        active_order = order
                        print(f"\U0001F4E4 Orden ejecutada tras reevaluación: {order.order_type.name} @ {order.entry_price}")

                        # Monitorear orden activamente
                        while active_order and active_order.status == order.status:
                            result = order_monitor.monitor_order(active_order)
                            if result:
                                decision_log.log_decision(
                                    symbol=active_order.symbol,
                                    decision_type="Order_Closed",
                                    signal=active_order.order_type.name,
                                    confidence=signal.confidence,
                                    reason="Orden cerrada por TP o SL",
                                    validated_by="Monitor"
                                )
                                print("✅ Orden cerrada. Esperando próximo análisis.")
                                active_order = None
                            time.sleep(15)
                else:
                    print("❌ Revalidación negativa. No se ejecuta orden.")

        except Exception as e:
            print(f"⚠️ Error detectado: {e}. Esperando para reeintentar...")
            time.sleep(15)


if __name__ == "__main__":
    main()
