from pydantic import Field
from pydantic_settings import BaseSettings


class RabbitMQConfig(BaseSettings):
    """RabbitMQ configuration settings."""

    rabbitmq_host: str = Field(
        default="rabbitmq",
        alias="RABBITMQ_HOST",
    )

    rabbitmq_port: int = Field(
        default=5672,
        alias="RABBITMQ_PORT",
    )

    rabbitmq_user: str = Field(
        default="guest",
        alias="RABBITMQ_USER",
    )

    rabbitmq_password: str = Field(
        default="guest",
        alias="RABBITMQ_PASSWORD",
    )

    @property
    def rabbitmq_url(self) -> str:
        """Build RabbitMQ connection URL."""
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"
