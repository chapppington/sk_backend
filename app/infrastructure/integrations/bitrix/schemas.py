from dataclasses import dataclass
from typing import Optional


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
