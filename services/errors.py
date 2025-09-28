import time
import drivers.ssd1306_float as ssd1306_float
from utils.logger import logger
from config import CONFIG

class ConnectionErrorBase(Exception):
    """Base class for device connection errors."""
    blink_count = 1

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class SensorConnectionError(ConnectionErrorBase):
    blink_count = CONFIG.SENSOR_CONNECTION_ERROR_BLINK_COUNT

class DisplayConnectionError(ConnectionErrorBase):
    blink_count = CONFIG.DISPLAY_CONNECTION_ERROR_BLINK_COUNT

def handle_connection_error(led, error: ConnectionErrorBase, screen_i2c=None):
    """
    Connection error indication:
    - logging
    - trying to display a message on the screen
    - blinking LED
    """
    logger.error(error.message)

    screen = None
    if screen_i2c:
        try:
            screen = ssd1306_float.SSD1306_I2C(CONFIG.DISPLAY_WIDTH,
                                               CONFIG.DISPLAY_HEIGHT,
                                               screen_i2c)
        except OSError as e:
            logger.error(f"Display init error: {e}")

    def draw_message():
        if not screen:
            return
        try:
            screen.fill(0)
            msg = error.message[:21]
            screen.text(msg, 0, 16)
            screen.show()
        except OSError as e:
            logger.error(f"Display writing error: {e}")

    for _ in range(20):
        draw_message()

        for _ in range(error.blink_count):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)

        time.sleep(1.5)
