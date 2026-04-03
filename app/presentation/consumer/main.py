import asyncio
import logging

import httpx
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from application.container import get_container
from infrastructure.integrations.bitrix.base import BaseBitrixClient
from infrastructure.integrations.email.base import BaseEmailClient
from infrastructure.integrations.email.templates_service import EmailTemplatesService
from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema
from presentation.consumer.converter import convert_event_to_lead_data
from settings.config import Config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

container = get_container()
config = container.resolve(Config)

broker = RabbitBroker(config.rabbitmq_url)

email_client = container.resolve(BaseEmailClient)
bitrix_client = container.resolve(BaseBitrixClient)

email_templates_service = EmailTemplatesService()
logger = logging.getLogger(__name__)


@broker.subscriber("submission_created")
async def submission_created_consumer(message: dict) -> None:
    event = SubmissionCreatedEventSchema(**message)

    if event.email:
        try:
            html_content = email_templates_service.render_submission_email(event)
            await email_client.send_email(
                to_email=event.email,
                subject=f"Новая заявка: {event.form_type}",
                body_html=html_content,
            )
        except Exception as e:
            print(e)

    try:
        lead_data = convert_event_to_lead_data(event)
        logger.info("Bitrix: отправка — %s (form_type=%s)", lead_data.title, event.form_type)
        lead_id = await bitrix_client.create_lead(lead_data)
        logger.info("Bitrix: статус отправки — успех, lead_id=%s", lead_id)
    except httpx.HTTPStatusError as e:
        logger.error(
            "Bitrix: статус отправки — ошибка HTTP %s, ответ: %s",
            e.response.status_code,
            (e.response.text[:1000] if e.response.text else "(пусто)"),
        )
        logger.exception("Bitrix: %s", e)
    except Exception as e:
        logger.error("Bitrix: статус отправки — ошибка: %s", e)
        logger.exception("Bitrix: %s", e)


if __name__ == "__main__":
    app = FastStream(broker)
    asyncio.run(app.run())
