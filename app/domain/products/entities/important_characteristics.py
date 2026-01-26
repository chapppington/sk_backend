from dataclasses import dataclass


@dataclass(frozen=True)
class ImportantCharacteristicUnit:
    text: str


@dataclass
class ImportantCharacteristicEntity:
    value: str
    unit: ImportantCharacteristicUnit | None = None
    description: str = ""
