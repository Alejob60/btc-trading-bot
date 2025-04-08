# ai_engine/decision_engine.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class DecisionEngine:
    def __init__(self):
        self.model = "gpt-4"

    def validate_signal_with_ai(self, signal) -> bool:
        prompt = (
            f"Validar señal: {signal.signal_type.name} para {signal.symbol}. Confianza: {signal.confidence}.\n"
            "¿Debe ejecutarse esta orden? Solo responde YES o NO."
        )
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.2
            )
            decision = response.choices[0].message.content.strip().upper()
            return decision == "YES"
        except Exception as e:
            print(f"⚠️ Error en validación IA: {e}")
            return False
