import requests

from config.settings import BOT_TOKEN


class TelegramService:

    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

    def send_message(self, chat_id: int, text: str):

        url = f"{self.BASE_URL}/sendMessage"

        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": False,
            },
            timeout=30,
        )

        return response.json()