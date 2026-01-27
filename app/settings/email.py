from pydantic import Field
from pydantic_settings import BaseSettings


class EmailConfig(BaseSettings):
    """Email configuration settings."""

    smtp_host: str = Field(
        default="maildev",
        alias="SMTP_HOST",
    )

    smtp_port: int = Field(
        default=1025,
        alias="SMTP_PORT",
    )

    smtp_user: str = Field(
        default="",
        alias="SMTP_USER",
    )

    smtp_password: str = Field(
        default="",
        alias="SMTP_PASSWORD",
    )

    smtp_use_tls: bool = Field(
        default=False,
        alias="SMTP_USE_TLS",
    )

    smtp_from_email: str = Field(
        default="noreply@example.com",
        alias="SMTP_FROM_EMAIL",
    )

    smtp_from_name: str = Field(
        default="SK Backend",
        alias="SMTP_FROM_NAME",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }
