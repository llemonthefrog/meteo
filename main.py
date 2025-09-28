from machine import Pin, I2C
import uasyncio as asyncio
import bme280
import ssd1306_float
import time

# pin connection testing
def test_conection(i2c_display: I2C, i2c_scanner: I2C) -> int:
    '''
    Scans pins and returns a status code 
    informing about errors or correct connection
    '''
    if(len(i2c_display.scan()) == 0):
        return 1
    
    elif(len(i2c_scanner.scan()) == 0):
        return 2
    
    return 0

def on_fail_connection(led: Pin, error_code: int, info: str, screen_i2c: I2C):
    """
    Notifies about an initialization error while connecting modules.
    Blinks LED 'error_code' times per cycle and, if available, shows 'info' on OLED.
    """
    screen = None
    try:
        screen = ssd1306_float.SSD1306_I2C(128, 64, screen_i2c)
    except:
        pass

    def draw_info():
        if not screen:
            return
        try:
            screen.fill(0)
            msg = info[:21]
            screen.text(msg, 0, 16)
            screen.show()
        except:
            pass

    for _ in range(20):
        draw_info()

        for _ in range(error_code):
            led.on()
            time.sleep(0.2)
            led.off()
            time.sleep(0.2)

        time.sleep(1.5)
#

temperature: float = 0.0
pressure: float = 0.0
humidity: float = 0.0

state_lock = asyncio.Lock() 

# async tasks
async def print_on_screen_data(screen: ssd1306_float.SSD1306_I2C):
    global temperature, pressure, humidity
    while True:
        async with state_lock:
            t = temperature
            p = pressure
            h = humidity

        screen.fill(0)
        screen.text("Temp: {:.1f} C".format(t), 0, 0)
        screen.text("Pres: {:.1f} hPa".format(p), 0, 16)
        screen.text("Hum:  {:.1f}%".format(h), 0, 32)
        screen.show()
        await asyncio.sleep(0.3)

def parse_bme_values(vals):
    def to_float(s):
        if isinstance(s, (int, float)):
            return float(s)
        out = []
        for ch in str(s):
            if ch.isdigit() or ch in ".-eE":
                out.append(ch)
        try:
            return float("".join(out))
        except:
            return float('nan')
    t, p, h = vals
    return to_float(t), to_float(p), to_float(h)

async def get_data(scanner: bme280.BME280):
    global temperature, pressure, humidity
    while True:
        t, p, h = parse_bme_values(scanner.values)
        async with state_lock:
            temperature, pressure, humidity = t, p, h
        await asyncio.sleep(0.3)
#

async def main(scanner: bme280.BME280, display: ssd1306_float.SSD1306_I2C):
    t1 = asyncio.create_task(get_data(scanner))
    t2 = asyncio.create_task(print_on_screen_data(display))
    await asyncio.gather(t1, t2)

def start():
    led = Pin("LED", Pin.OUT)
    i2c_scanner: I2C = I2C(0, scl=Pin(17), sda=Pin(16))
    i2c_display: I2C = I2C(1, scl=Pin(19), sda=Pin(18))

    code: int = test_conection(i2c_display=i2c_display, i2c_scanner=i2c_scanner)
    if(code == 2):
        on_fail_connection(led, code,"scanner problem", i2c_display)
        return
    elif(code == 1):
        on_fail_connection(led, code, "display problem", None)
        return

    scanner = bme280.BME280(i2c=i2c_scanner)
    display = ssd1306_float.SSD1306_I2C(128, 64, i2c_display)

    led.on()
    asyncio.run(main(scanner=scanner, display=display))
    led.off()

if __name__ == "__main__":
    start()
