from domain.weather_analyzer import predict_weather
from domain.models import WeatherData
from domain.ports import WeatherRepository

class WeatherService:
    def __init__(self, repo: WeatherRepository):
        self.repo = repo

    async def get_current(self) -> WeatherData | None:
        data = await self.repo.get_last(1)
        return data[0] if data else None

    async def predict(self) -> str:
        data = await self.repo.get_last_hours(3)
        return predict_weather(data)
    
    async def get_graph_data(
        self,
        hours: int = 6,
        segments: int = 12
    ) -> list[WeatherData]:
        return await self.repo.get_segmented_averages(hours, segments)
