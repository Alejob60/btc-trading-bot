# app/infrastructure/repositories/decision_log_repository.py
import os
from datetime import datetime

class DecisionLogRepository:
    def __init__(self, log_file_path: str = "logs/decision_log.log"):
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def log_decision(self, symbol: str, decision_type: str, signal: str, confidence: float, reason: str, validated_by: str = "None"):
        timestamp = datetime.now().isoformat()
        log_entry = (
            f"[{timestamp}] "
            f"SYMBOL: {symbol} | "
            f"TYPE: {decision_type} | "
            f"SIGNAL: {signal} | "
            f"CONFIDENCE: {confidence:.2f} | "
            f"REASON: {reason} | "
            f"VALIDATED_BY: {validated_by}\n"
        )
        with open(self.log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    
    def log_order(self, order, source="unknown"):
        from datetime import datetime
        path = "logs/decision_log.log"
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open(path, "a", encoding="utf-8") as log:
            log.write(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] decision_type=Order_Executed, symbol={order.symbol}, action={order.order_type.value}, price={order.entry_price}, tp={order.take_profit}, sl={order.stop_loss}, source={source}\n"
        )
