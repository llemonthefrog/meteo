import numpy as np

from .models import WeatherData

def analyze_trend(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0

    x = np.arange(len(values))
    y = np.array(values)
    a, _ = np.polyfit(x, y, 1)
    return float(a)


def predict_weather(data: list[WeatherData]) -> str:
    temps = [d.temperature for d in data]
    hums = [d.humidity for d in data]
    press = [d.pressure for d in data]

    avg_t = np.mean(temps)
    avg_h = np.mean(hums)
    avg_p = np.mean(press)
    trend_p = analyze_trend(press)

    if avg_h > 95 and avg_t < 7:
        return "🌫 Высокая вероятность тумана"

    if avg_t < 2 and avg_h > 85 and avg_p < 1008:
        return "🌫 Возможен снег"

    if avg_h > 85:
        if avg_p < 1005:
            return "🌧 Высокая вероятность дождя"
        if avg_p < 1008 and trend_p < 0:
            return "🌧 Возможен дождь"

    if avg_h < 70 and trend_p > 0:
        return "☀️ Осадков не ожидается"

    return "☀️ Погода стабильная, осадки маловероятны"
