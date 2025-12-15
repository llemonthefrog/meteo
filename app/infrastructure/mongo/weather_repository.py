import time
from motor.motor_asyncio import AsyncIOMotorClient

from domain.models import WeatherData
from domain.ports import WeatherRepository

class MongoWeatherRepository(WeatherRepository):
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]

    async def get_last(self, limit: int = 1) -> list[WeatherData]:
        cursor = (
            self.db.weather
            .find()
            .sort("timestamp", -1)
            .limit(limit)
        )

        docs = await cursor.to_list(length=limit)
        return [self._map(doc) for doc in docs]

    async def get_last_hours(self, hours: int = 3) -> list[WeatherData]:
        now = time.time()
        start = now - hours * 3600

        cursor = (
            self.db.weather
            .find({"timestamp": {"$gte": start}})
            .sort("timestamp", 1)
        )

        docs = await cursor.to_list(length=hours*120)
        return [self._map(doc) for doc in docs]
    
    async def get_segmented_averages(
        self,
        hours: int,
        segments: int
    ) -> list[WeatherData]:

        now = time.time()
        start = now - hours * 3600
        segment_seconds = (hours * 3600) / segments

        pipeline = [
            {"$match": {"timestamp": {"$gte": start}}},
            {"$project": {
                "temperature": 1,
                "humidity": 1,
                "pressure": 1,
                "segment": {
                    "$floor": {
                        "$divide": [
                            {"$subtract": ["$timestamp", start]},
                            segment_seconds
                        ]
                    }
                }
            }},
            {"$group": {
                "_id": "$segment",
                "avg_temp": {"$avg": "$temperature"},
                "avg_humidity": {"$avg": "$humidity"},
                "avg_pressure": {"$avg": "$pressure"}
            }},
            {"$sort": {"_id": 1}}
        ]

        docs = await self.db.weather.aggregate(pipeline).to_list(None)

        result = []
        for doc in docs:
            segment_start = start + doc["_id"] * segment_seconds
            result.append(
                WeatherData(
                    timestamp=segment_start,
                    temperature=doc["avg_temp"],
                    humidity=doc["avg_humidity"],
                    pressure=doc["avg_pressure"]
                )
            )

        return result


    def _map(self, doc: dict) -> WeatherData:
        return WeatherData(
            temperature=doc["temperature"],
            humidity=doc["humidity"],
            pressure=doc["pressure"],
            timestamp=doc["timestamp"],
        )
