from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from aiogram.types import BufferedInputFile
from zoneinfo import ZoneInfo

from domain.models import WeatherData

tz = ZoneInfo("Europe/Moscow")

def build_weather_graph(segments: list[WeatherData]) -> BufferedInputFile:
    times = [datetime.fromtimestamp(s.timestamp, tz) for s in segments]
    temps = [s.temperature for s in segments]
    hums = [s.humidity for s in segments]
    press = [s.pressure / 100 for s in segments]

    plt.figure(figsize=(10, 5))

    plt.plot(times, temps, label="Temperature (°C)")
    plt.plot(times, hums, label="Humidity (%)")
    plt.plot(times, press, label="Pressure (kPa)")

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%H:%M", tz=tz)
    )
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xlabel("Время")
    plt.ylabel("Значения")
    plt.title("Изменение погоды за последние часы")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()

    buf.seek(0)

    return BufferedInputFile(buf.read(), filename="weather.png")
