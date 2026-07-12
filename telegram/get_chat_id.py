import requests
from config.settings import BOT_TOKEN

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

response = requests.get(url)

print(response.json())