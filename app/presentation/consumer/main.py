import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema
from settings.rabbitmq import RabbitMQConfig


config = RabbitMQConfig()
broker = RabbitBroker(config.rabbitmq_url)


@broker.subscriber("submission_created")
async def submission_created_consumer(message: dict) -> None:
    event = SubmissionCreatedEventSchema(**message)
    print(
        f"Submission created - ID: {event.submission_id}, "
        f"Form Type: {event.form_type}, "
        f"Name: {event.name}, "
        f"Email: {event.email}, "
        f"Questionnaire Type: {event.questionnaire_type}, "
        f"Timestamp: {event.timestamp}",
    )


if __name__ == "__main__":
    app = FastStream(broker)
    asyncio.run(app.run())
