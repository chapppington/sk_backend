from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from settings.email import EmailConfig


class EmailClient:
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        body_html: str | None = None,
        from_email: str | None = None,
        from_name: str | None = None,
    ) -> None:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self._format_email_address(
            from_email or self.config.smtp_from_email,
            from_name or self.config.smtp_from_name,
        )
        message["To"] = to_email

        message.attach(MIMEText(body, "plain"))

        if body_html:
            message.attach(MIMEText(body_html, "html"))

        await self._send(message)

    async def _send(self, message: MIMEMultipart) -> None:
        await aiosmtplib.send(
            message,
            hostname=self.config.smtp_host,
            port=self.config.smtp_port,
            username=self.config.smtp_user if self.config.smtp_user else None,
            password=self.config.smtp_password if self.config.smtp_password else None,
            use_tls=self.config.smtp_use_tls,
        )

    @staticmethod
    def _format_email_address(email: str, name: str | None = None) -> str:
        if name:
            return f"{name} <{email}>"
        return email
