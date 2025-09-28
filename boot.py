

led = Pin("LED", Pin.OUT)
i2c_scanner: I2C = I2C(0, scl=Pin(17), sda=Pin(16))
i2c_display: I2C = I2C(1, scl=Pin(19), sda=Pin(18))