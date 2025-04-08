# app/infrastructure/repositories/trade_signal_repository.py
from app.domain.tradeSignal import TradeSignal

class TradeSignalRepository:
    def save(self, signal: TradeSignal):
        print(f"✅ Señal guardada: {signal.signal_type.name} para {signal.symbol} con confianza {signal.confidence}")
