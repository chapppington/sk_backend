import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from infrastructure.integrations.email.client import EmailClient
from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema
from settings.config import Config


config = Config()
broker = RabbitBroker(config.rabbitmq_url)
email_client = EmailClient(config=config)


def generate_submission_email_html(event: SubmissionCreatedEventSchema) -> str:
    files_list = ""
    if event.files:
        files_list = "<ul>"
        for file in event.files:
            files_list += f'<li><a href="{file}" style="color: #2563eb;">{file}</a></li>'
        files_list += "</ul>"
    else:
        files_list = "<p style='color: #6b7280;'>Файлы не прикреплены</p>"

    questionnaire_section = ""
    if event.questionnaire_type:
        questionnaire_section = f"""
        <div style="background: #f9fafb; padding: 16px; border-radius: 8px; margin-top: 16px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 12px 0; color: #111827; font-size: 16px; font-weight: 600;">
                Тип опросного листа
            </h3>
            <p style="margin: 0; color: #374151; font-size: 14px;">{event.questionnaire_type}</p>
        </div>
        """

    questionnaire_html_section = ""
    if event.questionnaire_html:
        questionnaire_html_section = f"""
        <div style="margin-top: 20px; margin-bottom: 20px;">
            <h3 style="margin: 0 0 16px 0; color: #111827; font-size: 18px; font-weight: 600; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                Опросный лист
            </h3>
            <div style="background: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb;">
                {event.questionnaire_html}
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Новая заявка</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                        <tr>
                            <td style="padding: 40px 40px 32px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px 12px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 700; text-align: center;">
                                    Новая заявка получена
                                </h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 32px 40px;">
                                <div style="margin-bottom: 24px;">
                                    <h2 style="margin: 0 0 8px 0; color: #111827; font-size: 20px; font-weight: 600;">
                                        Информация о заявке
                                    </h2>
                                    <p style="margin: 0; color: #6b7280; font-size: 14px;">
                                        ID заявки: <strong style="color: #111827;">{event.submission_id}</strong>
                                    </p>
                                </div>

                                <div style="background: #f9fafb; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #667eea;">
                                    <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                        <tr>
                                            <td style="padding: 8px 0; color: #6b7280; font-size: 14px; width: 140px;">
                                                Тип формы:
                                            </td>
                                            <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 600;">
                                                {event.form_type}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">
                                                Имя:
                                            </td>
                                            <td style="padding: 8px 0; color: #111827; font-size: 14px; font-weight: 600;">
                                                {event.name}
                                            </td>
                                        </tr>
                                        {
        f'''
                                        <tr>
                                            <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">
                                                Email:
                                            </td>
                                            <td style="padding: 8px 0;">
                                                <a href="mailto:{event.email}" style="color: #2563eb; text-decoration: none; font-size: 14px;">
                                                    {event.email}
                                                </a>
                                            </td>
                                        </tr>
                                        ''' if event.email else ''
    }
                                        {
        f'''
                                        <tr>
                                            <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">
                                                Телефон:
                                            </td>
                                            <td style="padding: 8px 0;">
                                                <a href="tel:{event.phone}" style="color: #2563eb; text-decoration: none; font-size: 14px;">
                                                    {event.phone}
                                                </a>
                                            </td>
                                        </tr>
                                        ''' if event.phone else ''
    }
                                        <tr>
                                            <td style="padding: 8px 0; color: #6b7280; font-size: 14px;">
                                                Дата создания:
                                            </td>
                                            <td style="padding: 8px 0; color: #111827; font-size: 14px;">
                                                {event.timestamp}
                                            </td>
                                        </tr>
                                    </table>
                                </div>

                                {
        f'''
                                <div style="margin-bottom: 20px;">
                                    <h3 style="margin: 0 0 12px 0; color: #111827; font-size: 16px; font-weight: 600;">
                                        Комментарий
                                    </h3>
                                    <div style="background: #f9fafb; padding: 16px; border-radius: 8px; border-left: 4px solid #10b981;">
                                        <p style="margin: 0; color: #374151; font-size: 14px; line-height: 1.6; white-space: pre-wrap;">
                                            {event.comments}
                                        </p>
                                    </div>
                                </div>
                                ''' if event.comments else ''
    }

                                <div style="margin-bottom: 20px;">
                                    <h3 style="margin: 0 0 12px 0; color: #111827; font-size: 16px; font-weight: 600;">
                                        Прикрепленные файлы
                                    </h3>
                                    <div style="background: #f9fafb; padding: 16px; border-radius: 8px;">
                                        {files_list}
                                    </div>
                                </div>

                                {questionnaire_section}

                                {questionnaire_html_section}

                                <div style="margin-top: 32px; padding-top: 24px; border-top: 1px solid #e5e7eb;">
                                    <p style="margin: 0; color: #6b7280; font-size: 12px; text-align: center;">
                                        Это автоматическое уведомление. Пожалуйста, не отвечайте на это письмо.
                                    </p>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def generate_submission_email_text(event: SubmissionCreatedEventSchema) -> str:
    text = f"""
Новая заявка получена

Информация о заявке:
ID заявки: {event.submission_id}
Тип формы: {event.form_type}
Имя: {event.name}
"""
    if event.email:
        text += f"Email: {event.email}\n"
    if event.phone:
        text += f"Телефон: {event.phone}\n"
    text += f"Дата создания: {event.timestamp}\n"

    if event.comments:
        text += f"\nКомментарий:\n{event.comments}\n"

    if event.files:
        text += "\nПрикрепленные файлы:\n"
        for file in event.files:
            text += f"- {file}\n"
    else:
        text += "\nФайлы не прикреплены\n"

    if event.questionnaire_type:
        text += f"\nТип опросного листа: {event.questionnaire_type}\n"

    return text


@broker.subscriber("submission_created")
async def submission_created_consumer(message: dict) -> None:
    event = SubmissionCreatedEventSchema(**message)

    if not event.email:
        return

    html_content = generate_submission_email_html(event)
    text_content = generate_submission_email_text(event)

    await email_client.send_email(
        to_email=event.email,
        subject=f"Новая заявка: {event.form_type}",
        body=text_content,
        body_html=html_content,
    )


if __name__ == "__main__":
    app = FastStream(broker)
    asyncio.run(app.run())
