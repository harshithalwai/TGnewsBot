import requests

from config.settings import BOT_TOKEN

class TelegramService:

    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def send_message(self, chat_id: int, message: str):

        url = f"{self.BASE_URL}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }

        response = requests.post(
            url,
            json=payload,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):
            raise RuntimeError(
                f"Telegram API error: {data}"
            )

        print(
            f"Telegram message sent successfully "
            f"to chat {chat_id}"
        )

        return data