import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from application.container import get_container
from infrastructure.integrations.bitrix.client import BitrixClient
from infrastructure.integrations.bitrix.converter import convert_event_to_lead_data
from infrastructure.integrations.email.client import EmailClient
from infrastructure.integrations.email.templates_service import EmailTemplatesService
from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema
from settings.config import Config


container = get_container()
config = container.resolve(Config)

broker = RabbitBroker(config.rabbitmq_url)

email_client = EmailClient(config=config)
email_templates_service = EmailTemplatesService()
bitrix_client = BitrixClient(config=config)


@broker.subscriber("submission_created")
async def submission_created_consumer(message: dict) -> None:
    event = SubmissionCreatedEventSchema(**message)

    if event.email:
        html_content = email_templates_service.render_submission_email(event)

        await email_client.send_email(
            to_email=event.email,
            subject=f"Новая заявка: {event.form_type}",
            body_html=html_content,
        )

    try:
        lead_data = convert_event_to_lead_data(event)
        await bitrix_client.create_lead(lead_data)
    except Exception:
        pass


if __name__ == "__main__":
    app = FastStream(broker)
    asyncio.run(app.run())
