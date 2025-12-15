from app.domain.weather_analyzer import predict_weather
from app.domain.models import WeatherData

def test_predict_fog():
    data_fog = [
        WeatherData(temperature=(5.0 - i * 0.1), humidity=(96.0 + i * 0.1), pressure=1012.0, timestamp=i)
        for i in range(20)
    ]

    result = predict_weather(data_fog)
    assert result == "🌫 Высокая вероятность тумана"

def test_predict_high_rain():
    data_rain_high = [
        WeatherData(temperature=12.0, humidity=(86.0 + i * 0.2), pressure=1004.0, timestamp=i)
        for i in range(20)
    ]

    result = predict_weather(data_rain_high)
    assert result == "🌧 Высокая вероятность дождя"

def test_predict_small_rain():
    data_rain_trend = [
        WeatherData(
            temperature=14.0,
            humidity=88.0,
            pressure=(1010 - i * 0.3),
            timestamp=i
        )
        for i in range(20)
    ] 

    result = predict_weather(data_rain_trend)
    assert result == "🌧 Возможен дождь"

def test_predict_snow():
    data_snow = [
        WeatherData(
            temperature=(2 - i * 0.1),
            humidity=(86.0 + i * 0.1),
            pressure=(1008.0 - i * 0.1),
            timestamp=i
        )
        for i in range(20)
    ]

    result = predict_weather(data_snow)
    assert result == "🌫 Возможен снег"

def test_clear_weather():
    data_clear = [
        WeatherData(
            temperature=18.0,
            humidity=55.0,
            pressure=(1008 + i * 0.4),
            timestamp=i
        )
        for i in range(20)
    ]

    result = predict_weather(data_clear)
    assert result == "☀️ Осадков не ожидается"

def test_stable_weather():
    data_stable = [
        WeatherData(
            temperature=15.0,
            humidity=75.0,
            pressure=1012.0,
            timestamp=i
        )
        for i in range(20)
    ]

    result = predict_weather(data_stable)
    assert result == "☀️ Погода стабильная, осадки маловероятны"
