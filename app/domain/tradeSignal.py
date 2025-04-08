# app/domain/trade_signal.py
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

@dataclass
class TradeSignal:
    symbol: str
    signal_type: SignalType
    confidence: float  # Rango de 0.0 a 1.0
    reason: str
    generated_at: datetime
