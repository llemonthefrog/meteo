import uasyncio as asyncio
from .state import SensorData

async def update_display(screen, state: SensorData, interval: float):
    while True:
        async with state.lock:
            t, p, h = state.temperature, state.pressure, state.humidity

        screen.fill(0)
        screen.text(f"Temp: {t:.1f} C", 0, 0)
        screen.text(f"Pres: {p:.1f} hPa", 0, 16)
        screen.text(f"Hum:  {h:.1f}%", 0, 32)
        screen.show()
            
        await asyncio.sleep(interval)
