# app/domain/order.py
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"

@dataclass
class Order:
    symbol: str
    order_type: OrderType
    amount: float
    entry_price: float
    take_profit: float
    stop_loss: float
    status: OrderStatus
    opened_at: datetime
    closed_at: datetime = None
