# main.py
from app.infrastructure.market_data_provider import MarketDataProvider
from app.infrastructure.repositories.trade_signal_repository import TradeSignalRepository
from app.infrastructure.repositories.decision_log_repository import DecisionLogRepository
from app.services.trading_bot_service import TradingBotService
from app.services.order_monitor import OrderMonitor
from ai_engine.decision_engine import DecisionEngine


def main():
    print("🚀 Iniciando bot de trading para BTC/USDT (LIVE MODE)...")

    # Componentes
    market_data_provider = MarketDataProvider()
    trade_signal_repo = TradeSignalRepository()
    bot_service = TradingBotService()
    order_monitor = OrderMonitor()
    decision_engine = DecisionEngine()
    decision_log = DecisionLogRepository()

    # 1. Obtener datos del mercado desde Binance
    market_data = market_data_provider.get_latest_market_data()
    print(f"📊 Datos del mercado real: {market_data}")

    # 2. Analizar y generar señal
    signal = bot_service.analyze_market(market_data)
    print(f"📈 Señal generada: {signal.signal_type.name} con confianza {signal.confidence}")

    # 3. Guardar señal en repositorio y log
    trade_signal_repo.save(signal)
    decision_log.log_decision(
        symbol=signal.symbol,
        decision_type="Technical",
        signal=signal.signal_type.name,
        confidence=signal.confidence,
        reason=signal.reason,
        validated_by="System"
    )

    # 4. Validar con IA antes de ejecutar
    if signal.signal_type.name in ["BUY", "SELL"]:
        if decision_engine.validate_signal_with_ai(signal):
            decision_log.log_decision(
                symbol=signal.symbol,
                decision_type="AI_Validated",
                signal=signal.signal_type.name,
                confidence=signal.confidence,
                reason=signal.reason,
                validated_by="ChatGPT + DeepSeek"
            )

            order = bot_service.execute_trade(signal)
            print(f"📤 Orden simulada: {order.order_type.name} {order.symbol} @ {order.entry_price} ✅")
            order_monitor.monitor(order)
            decision_log.log_decision(
            symbol=order.symbol,
            decision_type="Order_Executed",
            signal=order.order_type.name,
            confidence=signal.confidence,
            reason=f"ENTRY: {order.entry_price}, TP: {order.take_profit}, SL: {order.stop_loss}",
            validated_by="Bot"
        )
        else:
            print("❌ Orden bloqueada por IA. No se ejecutará.")
            decision_log.log_decision(
                symbol=signal.symbol,
                decision_type="AI_Rejected",
                signal=signal.signal_type.name,
                confidence=signal.confidence,
                reason=signal.reason,
                validated_by="ChatGPT + DeepSeek"
            )

if __name__ == "__main__":
    main()
