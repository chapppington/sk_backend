from pydantic import Field
from pydantic_settings import BaseSettings


class BitrixConfig(BaseSettings):
    """Bitrix24 configuration settings."""

    bitrix_webhook_url: str = Field(
        default="",
        alias="BITRIX_WEBHOOK_URL",
        description="URL вебхука Bitrix24 для API запросов",
    )

    bitrix_assigned_by_id: int = Field(
        default=2,
        alias="BITRIX_ASSIGNED_BY_ID",
        description="ID ответственного пользователя в Bitrix24",
    )
