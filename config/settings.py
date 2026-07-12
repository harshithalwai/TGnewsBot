from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = {
    "host": os.getenv("DATABASE_HOST"),
    "port": os.getenv("DATABASE_PORT"),
    "database": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
}

BOT_TOKEN = os.getenv("BOT_TOKEN")