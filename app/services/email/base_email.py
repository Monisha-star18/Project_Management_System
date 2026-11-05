
from abc import ABC, abstractmethod

import httpx

from app.core.config import get_settings
from app.utilites.logger import logger


class BaseEmail(ABC):

    MAILJET_URL = "https://api.mailjet.com/v3.1/send"

    def __init__(self, sender_email: str | None = None):
        settings = get_settings()

        self.sender_email = (
            sender_email or settings.mailjet_sender_email
        )

    @abstractmethod
    def build_message(self, full_name: str) -> tuple[str, str]:
        """Return the email subject and body."""
        pass

    async def send(self, email: str, full_name: str) -> None:
        settings = get_settings()

        subject, body = self.build_message(full_name)

        payload = {
            "Messages": [
                {
                    "From": {
                        "Email": self.sender_email,
                        "Name": settings.mailjet_sender_name,
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": full_name,
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body,
                }
            ]
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                self.MAILJET_URL,
                auth=(
                    settings.mailjet_api_key,
                    settings.mailjet_secret_key,
                ),
                json=payload,
            )

            response.raise_for_status()

            for message in response.json().get("Messages", []):
                if message.get("Status") != "success":
                    raise RuntimeError("Mailjet rejected the email")
