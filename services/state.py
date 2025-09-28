from dataclasses import dataclass
import uasyncio as asyncio

@dataclass
class SensorData:
    temperature: float = 0.0
    pressure: float = 0.0
    humidity: float = 0.0
    
    lock: asyncio.Lock = asyncio.Lock()
