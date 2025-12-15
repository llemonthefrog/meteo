from dataclasses import dataclass

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    pressure: float
    timestamp: float
