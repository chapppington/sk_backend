from abc import (
    ABC,
    abstractmethod,
)

from infrastructure.integrations.bitrix.schemas import BitrixLeadData


class BaseBitrixClient(ABC):
    @abstractmethod
    async def create_lead(self, lead_data: BitrixLeadData) -> int: ...
