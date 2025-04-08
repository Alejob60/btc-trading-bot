# main.py
import time
from app.infrastructure.market_data_provider import MarketDataProvider
from app.infrastructure.repositories.trade_signal_repository import TradeSignalRepository
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository
from app.services.trading_bot_service import TradingBotService
from app.services.order_monitor import OrderMonitor
from ai_engine.decision_engine import DecisionEngine
from app.services.predictive_model_service import PredictiveModelService


def main():
    print("🚀 Bot de trading para BTC/USDT ejecutándose en MODO CONSERVADOR...")

    # Componentes
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
            if active_order and active_order.status.name == "OPEN":
                print("🔄 Monitoreando orden activa... Esperando próximo análisis...")
                order_monitor.monitor(active_order)
                if active_order.status.name == "CLOSED":
                    active_order = None
                time.sleep(60)
                continue

            # Obtener precio y velas largas
            current_price = market_data_provider.get_current_price("BTCUSDT")
            print(f"📊 Precio actual: {current_price}")

            recent_candles = market_data_provider.get_recent_candles(symbol="BTCUSDT", interval="1m", limit=60)
            predictive_result = predictive_model.analyze(recent_candles)
            print(f"🧠 Predicción IA: {predictive_result}")

            market_data = market_data_provider.get_latest_market_data()
            signal = bot_service.analyze_market(market_data)
            print(f"📈 Señal técnica: {signal.signal_type.name}, confianza: {signal.confidence}")

            if predictive_result["decision"] != signal.signal_type.name:
                print("⏸️ Señales no coinciden, reevaluando con IA...")
                reevaluated = decision_engine.revalidate_with_context(signal, recent_candles)
                if not reevaluated:
                    print("🔒 IA bloqueó la señal tras reevaluación. Esperando próximo ciclo.")
                    time.sleep(60)
                    continue

            if signal.signal_type.name in ["BUY", "SELL"]:
                trade_signal_repo.save(signal)
                decision_log.log_decision(
                    symbol=signal.symbol,
                    decision_type="Conservative_Validated",
                    signal=signal.signal_type.name,
                    confidence=signal.confidence,
                    reason="Confirmado tras reevaluación IA + técnica",
                    validated_by="ChatGPT"
                )
                order = bot_service.execute_trade(signal, current_price=current_price, dry_run=True)
                print(f"📤 Orden ejecutada: {order.order_type.name} @ {order.entry_price}")
                active_order = order
                order_monitor.monitor(active_order)

                decision_log.log_decision(
                    symbol=order.symbol,
                    decision_type="Order_Executed",
                    signal=order.order_type.name,
                    confidence=signal.confidence,
                    reason=f"TP: {order.take_profit}, SL: {order.stop_loss}",
                    validated_by="Bot"
                )
            else:
                print("⏸️ HOLD - No se genera señal ni orden")

        except Exception as e:
            print(f"⚠️ Error detectado: {e}. Esperando para reeintentar...")

        time.sleep(60)


if __name__ == "__main__":
    main()
