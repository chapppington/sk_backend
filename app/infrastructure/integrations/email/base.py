from abc import (
    ABC,
    abstractmethod,
)


class BaseEmailClient(ABC):
    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body_html: str,
        from_email: str | None = None,
        from_name: str | None = None,
    ) -> None: ...
