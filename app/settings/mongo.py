from pydantic import Field
from pydantic_settings import BaseSettings


class MongoConfig(BaseSettings):
    """MongoDB configuration settings."""

    mongo_host: str = Field(
        default="mongodb",
        alias="MONGO_HOST",
    )

    mongo_port: int = Field(
        default=27017,
        alias="MONGO_PORT",
    )

    mongo_user: str = Field(
        default="admin",
        alias="MONGO_ROOT_USER",
    )

    mongo_password: str = Field(
        default="admin",
        alias="MONGO_ROOT_PASSWORD",
    )

    mongo_database: str = Field(
        default="sk",
        alias="MONGO_DATABASE",
    )

    @property
    def mongo_connection_url(self) -> str:
        return f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/{self.mongo_database}?authSource=admin"
