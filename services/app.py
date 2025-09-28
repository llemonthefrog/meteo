import uasyncio as asyncio
import drivers.bme280 as bme280
import drivers.ssd1306_float as ssd1306_float
from .state import SensorData
from .sensors import poll_sensor
from .display import update_display
from utils.logger import logger
from config import CONFIG

class WeatherApp:
    def __init__(self, i2c_scanner, i2c_display):
        self.state = SensorData()
        try:
            self.sensor = bme280.BME280(i2c=i2c_scanner)
            logger.info("Sensor initialized")
        except OSError as e:
            logger.error(f"Sensor init failed: {e}")
            raise

        try:
            self.display = ssd1306_float.SSD1306_I2C(CONFIG.DISPLAY_WIDTH,
                                                     CONFIG.DISPLAY_HEIGHT,
                                                     i2c_display)
            logger.info("Display initialized")
        except OSError as e:
            logger.error(f"Display init failed: {e}")
            raise

    async def run(self):
        logger.info("Application started")
        tasks = [
            asyncio.create_task(poll_sensor(self.sensor, self.state, CONFIG.UPDATE_INTERVAL)),
            asyncio.create_task(update_display(self.display, self.state, CONFIG.UPDATE_INTERVAL))
        ]
        await asyncio.gather(*tasks)
