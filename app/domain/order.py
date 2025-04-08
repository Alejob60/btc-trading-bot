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

    def __str__(self):
        return (f"Order(symbol={self.symbol}, order_type={self.order_type}, amount={self.amount}, "
                f"entry_price={self.entry_price}, take_profit={self.take_profit}, stop_loss={self.stop_loss}, "
                f"status={self.status}, opened_at={self.opened_at}, closed_at={self.closed_at})")

    def get_side(self):
        # Devuelve el tipo de orden como 'BUY' o 'SELL'
        return self.order_type.value
