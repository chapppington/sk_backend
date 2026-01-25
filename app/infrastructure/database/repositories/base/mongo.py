from abc import ABC
from dataclasses import dataclass

from infrastructure.database.gateways.mongo import MongoDatabase


@dataclass
class BaseMongoRepository(ABC):
    mongo_database: MongoDatabase
    collection_name: str

    @property
    def collection(self):
        return self.mongo_database.connection[self.collection_name]
