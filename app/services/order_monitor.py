# app/services/order_monitor.py

import threading
import time
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv
import os
from app.domain.order import Order, OrderStatus

load_dotenv()

class OrderMonitor:
    def __init__(self):
        self.client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_SECRET_KEY"))

    def monitor(self, order: Order, interval: int = 10):
        def run():
            print(f"🕒 Iniciando monitoreo de orden: {order.order_type.name} {order.symbol}...")
            while order.status == OrderStatus.OPEN:
                ticker = self.client.get_symbol_ticker(symbol=order.symbol)
                current_price = float(ticker['price'])
                print(f"📡 Precio actual: {current_price} | TP: {order.take_profit:.2f} | SL: {order.stop_loss:.2f}")

                if order.order_type.name == "BUY":
                    if current_price >= order.take_profit:
                        print("🎯 ¡Take Profit alcanzado! Cerrando orden.")
                        order.status = OrderStatus.CLOSED
                        order.closed_at = datetime.now()
                        break
                    elif current_price <= order.stop_loss:
                        print("🛑 ¡Stop Loss alcanzado! Cerrando orden.")
                        order.status = OrderStatus.CLOSED
                        order.closed_at = datetime.now()
                        break
                else:  # SELL
                    if current_price <= order.take_profit:
                        print("🎯 ¡Take Profit alcanzado (venta)! Cerrando orden.")
                        order.status = OrderStatus.CLOSED
                        order.closed_at = datetime.now()
                        break
                    elif current_price >= order.stop_loss:
                        print("🛑 ¡Stop Loss alcanzado (venta)! Cerrando orden.")
                        order.status = OrderStatus.CLOSED
                        order.closed_at = datetime.now()
                        break

                time.sleep(interval)

        thread = threading.Thread(target=run)
        thread.start()
        return thread
