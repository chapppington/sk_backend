from dataclasses import dataclass


@dataclass
class AdvantageEntity:
    label: str
    icon: str
    image: str | None = None
    alt: str | None = None
    description: str = ""
