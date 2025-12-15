import asyncio
import os

from aiogram import Bot, Dispatcher
from infrastructure.mongo.weather_repository import MongoWeatherRepository
from application.weather_service import WeatherService
from presentation.telegram.handlers import router

async def main():
    repo: MongoWeatherRepository = MongoWeatherRepository(os.getenv("MONGO_URI"), "weather_db")
    service: WeatherService = WeatherService(repo=repo)
    
    dispatcher: Dispatcher = Dispatcher()
    dispatcher.workflow_data["weather_service"] = service
    dispatcher.include_router(router=router)

    bot = Bot(os.getenv("TG_TOKEN"))
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    