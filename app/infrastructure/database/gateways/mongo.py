from motor.motor_asyncio import AsyncIOMotorClient


class MongoDatabase:
    def __init__(self, mongo_url: str, mongo_database: str):
        self._client = AsyncIOMotorClient(mongo_url)
        self._connection = self._client.get_database(mongo_database)

    @property
    def connection(self):
        return self._connection
