import uasyncio as asyncio
from utils.parser import parse_bme_values
from .state import SensorData

async def poll_sensor(sensor, state: SensorData, interval: float):
    """
    Reads data from BME280 and updates state.
    """
    while True:
        t, p, h = parse_bme_values(sensor.values)
        async with state.lock:
            state.temperature, state.pressure, state.humidity = t, p, h

        await asyncio.sleep(interval)
