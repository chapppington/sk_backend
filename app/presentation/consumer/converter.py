from infrastructure.integrations.bitrix.client import BitrixLeadData
from presentation.api.v1.submissions.schemas import SubmissionCreatedEventSchema


def convert_event_to_lead_data(event: SubmissionCreatedEventSchema) -> BitrixLeadData:
    """Конвертирует событие создания заявки в данные для лида Bitrix24."""
    title_map = {
        "Опросный лист": "Опросный лист с сайта",
        "Обращение": "Обращение с сайта",
    }
    title = title_map.get(event.form_type, "Заявка с сайта")

    lead_comments = event.comments or ""

    if event.answers_file_url:
        lead_comments += "\n\n=== Файл с ответами опросного листа ===\n"
        lead_comments += event.answers_file_url

    if event.files:
        lead_comments += "\n\n=== Прикрепленные файлы ===\n"
        for file in event.files:
            lead_comments += f"{file}\n"

    name_parts = event.name.split(" ")
    first_name = name_parts[0] if name_parts else event.name
    last_name = name_parts[-1] if len(name_parts) > 1 else None
    second_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else None

    return BitrixLeadData(
        title=title,
        name=first_name,
        last_name=last_name,
        second_name=second_name,
        email=event.email,
        phone=event.phone,
        comments=lead_comments.strip() if lead_comments.strip() else None,
    )
