# app/services/ai_predictor.py

import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

class AIPredictor:
    def __init__(self):
        self.model_gpt = "gpt-4"
        self.model_deepseek = "deepseek-chat"

    def format_candles_for_prompt(self, candles):
        return "\n".join([
            f"{i+1}. O:{c['open']} H:{c['high']} L:{c['low']} C:{c['close']}"
            for i, c in enumerate(candles)
        ])

    def predict_with_chatgpt(self, candles) -> str:
        prompt = (
            "Dado el siguiente historial de velas OHLC de BTCUSDT, predice si la próxima vela será UP o DOWN. Solo responde: UP o DOWN.\n"
            f"{self.format_candles_for_prompt(candles)}"
        )
        try:
            response = openai.chat.completions.create(
                model=self.model_gpt,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.2
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"⚠️ Error con ChatGPT: {e}")
            return "ERROR"

    def validate_signal_with_chatgpt(self, signal) -> bool:
        prompt = (
            f"Señal para {signal.symbol}: {signal.signal_type.name} con confianza {signal.confidence}. Ejecutar orden? Solo responde YES o NO."
        )
        try:
            response = openai.chat.completions.create(
                model=self.model_gpt,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
                temperature=0.2
            )
            answer = response.choices[0].message.content.strip().upper()
            return answer == "YES"
        except Exception as e:
            print(f"⚠️ Error en validación con ChatGPT: {e}")
            return False

    def predict_with_deepseek(self, candles) -> str:
        prompt = (
            "Velas OHLC recientes de BTCUSDT. ¿Dirección siguiente vela? Solo responde: UP o DOWN\n"
            f"{self.format_candles_for_prompt(candles)}"
        )
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_deepseek,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 5,
            "temperature": 0.2
        }

        try:
            res = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
            result = res.json()
            return result['choices'][0]['message']['content'].strip().upper()
        except Exception as e:
            print(f"⚠️ Error con DeepSeek: {e}")
            return "ERROR"
