from machine import Pin, I2C
import uasyncio as asyncio
from config import CONFIG
from services.errors import (
    handle_connection_error,
    SensorConnectionError,
    DisplayConnectionError,
)
from services.app import WeatherApp

def check_connections(i2c_display: I2C, i2c_scanner: I2C):
    """
    Checks device connections.
    Throws an exception if any connection failed.
    """
    if not i2c_display.scan():
        raise DisplayConnectionError("Display connection failed")
    if not i2c_scanner.scan():
        raise SensorConnectionError("Sensor connection failed")

def start():
    led = Pin(CONFIG.LED_PIN, Pin.OUT)

    i2c_scanner = I2C(CONFIG.I2C_SCANNER_ID,
                      scl=Pin(CONFIG.I2C_SCANNER_SCL),
                      sda=Pin(CONFIG.I2C_SCANNER_SDA))
    i2c_display = I2C(CONFIG.I2C_DISPLAY_ID,
                      scl=Pin(CONFIG.I2C_DISPLAY_SCL),
                      sda=Pin(CONFIG.I2C_DISPLAY_SDA))

    try:
        check_connections(i2c_display, i2c_scanner)
        app = WeatherApp(i2c_scanner, i2c_display)
        led.on()
        asyncio.run(app.run())
    except (SensorConnectionError, DisplayConnectionError) as e:
        handle_connection_error(led, e, i2c_display)
    finally:
        led.off()

if __name__ == "__main__":
    start()
