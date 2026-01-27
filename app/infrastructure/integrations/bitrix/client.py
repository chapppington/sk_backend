from dataclasses import dataclass
from typing import (
    Any,
    Optional,
)

import httpx

from settings.config import Config


@dataclass
class BitrixLeadData:
    title: str
    name: str
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    comments: Optional[str] = None
    company_title: Optional[str] = None
    address_city: Optional[str] = None
    web: Optional[str] = None


class BitrixClient:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.webhook_url = config.bitrix_webhook_url
        self.timeout = 30.0

    async def create_lead(self, lead_data: BitrixLeadData) -> int:
        """Создает лид в Bitrix24."""
        fields: dict[str, Any] = {
            "TITLE": lead_data.title,
            "ASSIGNED_BY_ID": self.config.bitrix_assigned_by_id,
            "NAME": lead_data.name,
            "OPENED": "Y",
            "STATUS_ID": "NEW",
            "SOURCE_ID": "WEB",
        }

        if lead_data.last_name:
            fields["LAST_NAME"] = lead_data.last_name
        if lead_data.second_name:
            fields["SECOND_NAME"] = lead_data.second_name
        if lead_data.company_title:
            fields["COMPANY_TITLE"] = lead_data.company_title
        if lead_data.address_city:
            fields["ADDRESS_CITY"] = lead_data.address_city
        if lead_data.comments:
            fields["COMMENTS"] = lead_data.comments

        if lead_data.email:
            fields["EMAIL"] = [
                {
                    "VALUE": lead_data.email,
                    "VALUE_TYPE": "WORK",
                },
            ]

        if lead_data.phone:
            fields["PHONE"] = [
                {
                    "VALUE": lead_data.phone,
                    "VALUE_TYPE": "WORK",
                },
            ]

        if lead_data.web:
            fields["WEB"] = [
                {
                    "VALUE": lead_data.web,
                    "VALUE_TYPE": "WORK",
                },
            ]

        request_data = {
            "fields": fields,
            "params": {
                "REGISTER_SONET_EVENT": "Y",
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.webhook_url}/crm.lead.add.json",
                json=request_data,
                headers={
                    "Content-Type": "application/json",
                },
            )

            response.raise_for_status()
            response_data = response.json()

        if response_data and "result" in response_data:
            return response_data["result"]

        raise ValueError("Bitrix24 вернул неожиданный формат ответа")
