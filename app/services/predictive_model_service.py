# app/services/predictive_model_service.py

from app.services.pattern_detector import PatternDetector
from app.services.ai_predictor import AIPredictor

class PredictiveModelService:
    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.ai_predictor = AIPredictor()

    def analyze(self, candles: list[dict]) -> dict:
        if not candles or len(candles) < 5:
            return {"decision": "HOLD", "confidence": 0.0, "patterns": [], "reason": "Insufficient data"}

        # 1. Detectar patrones técnicos
        patterns = self.pattern_detector.detect(candles)

        # 2. Obtener predicción de IA
        gpt_prediction = self.ai_predictor.predict_with_chatgpt(candles)
        ds_prediction = self.ai_predictor.predict_with_deepseek(candles)

        # 3. Evaluar decisión combinada
        up_votes = [gpt_prediction, ds_prediction].count("UP")
        down_votes = [gpt_prediction, ds_prediction].count("DOWN")

        if up_votes > down_votes:
            decision = "BUY"
            confidence = 0.7 if patterns else 0.6
        elif down_votes > up_votes:
            decision = "SELL"
            confidence = 0.7 if patterns else 0.6
        else:
            decision = "HOLD"
            confidence = 0.5

        return {
            "decision": decision,
            "confidence": confidence,
            "patterns": patterns,
            "reason": f"GPT: {gpt_prediction}, DeepSeek: {ds_prediction}, Patterns: {', '.join(patterns) if patterns else 'None'}"
        }
