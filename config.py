from dataclasses import dataclass
from machine import Pin

@dataclass(frozen=True)
class Config:
    # --- I2C ---
    I2C_SCANNER_ID: int = 0
    I2C_SCANNER_SCL: int = 17
    I2C_SCANNER_SDA: int = 16

    I2C_DISPLAY_ID: int = 1
    I2C_DISPLAY_SCL: int = 19
    I2C_DISPLAY_SDA: int = 18

    # --- LED ---
    LED_PIN: str = "LED"

    # --- Intervals ---
    UPDATE_INTERVAL: float = 0.3  # seconds

    # --- Display ---
    DISPLAY_WIDTH: int = 128
    DISPLAY_HEIGHT: int = 64

    # --- Error indication ---
    SENSOR_CONNECTION_ERROR_BLINK_COUNT: int = 2
    DISPLAY_CONNECTION_ERROR_BLINK_COUNT: int = 3

CONFIG = Config()
