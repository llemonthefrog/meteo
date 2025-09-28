import uasyncio as asyncio
from utils.parser import parse_bme_values
from utils.logger import logger
from .state import SensorData

async def poll_sensor(sensor, state: SensorData, interval: float):
    """
    Reads data from BME280 and updates state.
    """
    while True:
        try:
            t, p, h = parse_bme_values(sensor.values)
            async with state.lock:
                state.temperature, state.pressure, state.humidity = t, p, h
            logger.debug(f"Sensor data: T={t:.2f} P={p:.2f} H={h:.2f}")
        except OSError as e:
            logger.error(f"Sensor read error: {e}")
        await asyncio.sleep(interval)
