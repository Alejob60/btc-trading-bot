# ai_engine/decision_engine.py

import os
from openai import OpenAI

class DecisionEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def validate_signal_with_ai(self, signal):
        prompt = f"""
        Valida esta señal de trading de BTC/USDT.
        Señal técnica: {signal.signal_type.name}
        Confianza: {signal.confidence}
        Motivo: {signal.reason}
        ¿Es una buena operación en base a análisis técnico? Responde: APROBADA o RECHAZADA.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            content = response.choices[0].message.content.upper()
            return "APROBADA" in content
        except Exception as e:
            print(f"⚠️ Error validando con IA: {e}")
            return False

    def revalidate_with_context(self, signal, candles):
        """
        Realiza una reevaluación en profundidad con contexto extendido (velas de 1 hora).
        """
        pattern_info = "\n".join([
            f"Open: {c['open']}, High: {c['high']}, Low: {c['low']}, Close: {c['close']}"
            for c in candles[-20:]
        ])

        prompt = f"""
        Eres un experto en trading de criptomonedas. Aquí tienes los últimos datos de 20 velas de 1 minuto:

        {pattern_info}

        Basado en el contexto anterior, analiza la siguiente señal:
        - Tipo: {signal.signal_type.name}
        - Confianza: {signal.confidence}
        - Motivo original: {signal.reason}

        ¿Consideras que esta señal sigue siendo válida para ejecutar una orden de trading ahora?
        Responde solo con APROBADA o RECHAZADA.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            decision = response.choices[0].message.content.strip().upper()
            return "APROBADA" in decision
        except Exception as e:
            print(f"⚠️ Error en reevaluación con IA: {e}")
            return False
