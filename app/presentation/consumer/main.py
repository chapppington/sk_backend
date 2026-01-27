import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from application.container import get_container
from infrastructure.integrations.email.client import EmailClient
from infrastructure.integrations.email.templates_service import EmailTemplatesService
from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema
from settings.config import Config


container = get_container()
config = container.resolve(Config)
broker = RabbitBroker(config.rabbitmq_url)
email_client = EmailClient(config=config)
email_templates_service = EmailTemplatesService()


@broker.subscriber("submission_created")
async def submission_created_consumer(message: dict) -> None:
    event = SubmissionCreatedEventSchema(**message)

    if not event.email:
        return

    html_content = email_templates_service.render_submission_email(event)

    await email_client.send_email(
        to_email=event.email,
        subject=f"Новая заявка: {event.form_type}",
        body_html=html_content,
    )


if __name__ == "__main__":
    app = FastStream(broker)
    asyncio.run(app.run())
