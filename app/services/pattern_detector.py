# app/services/pattern_detector.py

class PatternDetector:

    def detect(self, candles: list[dict]) -> list[str]:
        patterns_found = []

        if not candles or len(candles) < 2:
            return patterns_found

        last = candles[-1]
        prev = candles[-2]

        # Patrón 1: Martillo (Hammer)
        if last['close'] > last['open'] and (last['open'] - last['low']) > 2 * (last['close'] - last['open']):
            patterns_found.append("Hammer")

        # Patrón 2: Envolvente alcista
        if prev['close'] < prev['open'] and last['close'] > last['open'] and last['close'] > prev['open'] and last['open'] < prev['close']:
            patterns_found.append("Bullish Engulfing")

        # Patrón 3: Envolvente bajista
        if prev['close'] > prev['open'] and last['close'] < last['open'] and last['open'] > prev['close'] and last['close'] < prev['open']:
            patterns_found.append("Bearish Engulfing")

        # Patrón 4: Doji
        if abs(last['close'] - last['open']) <= ((last['high'] - last['low']) * 0.1):
            patterns_found.append("Doji")

        return patterns_found
