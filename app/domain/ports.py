from abc import ABC, abstractmethod
from .models import WeatherData

class WeatherRepository(ABC):

    @abstractmethod
    async def get_last(self, limit: int) -> list[WeatherData]:
        pass

    @abstractmethod
    async def get_last_hours(self, hours: int) -> list[WeatherData]:
        pass

    @abstractmethod
    async def get_segmented_averages(self, hours: int, segments: int) -> list[WeatherData]:
        pass
