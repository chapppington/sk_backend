from abc import ABC
from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from uuid import (
    UUID,
    uuid4,
)
from zoneinfo import ZoneInfo


BARNAUL_TZ = ZoneInfo("Asia/Barnaul")


def _now_barnaul() -> datetime:
    return datetime.now(tz=BARNAUL_TZ)


@dataclass
class BaseEntity(ABC):
    oid: UUID = field(default_factory=uuid4, kw_only=True)
    created_at: datetime = field(default_factory=_now_barnaul, kw_only=True)
    updated_at: datetime = field(default_factory=_now_barnaul, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, other: "BaseEntity") -> bool:
        return self.oid == other.oid
