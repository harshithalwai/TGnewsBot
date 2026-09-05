from dotenv import load_dotenv
import os


load_dotenv()


DATABASE = {

    "host": os.getenv(
        "DATABASE_HOST",
        "localhost",
    ),

    "port": os.getenv(
        "DATABASE_PORT",
        "5432",
    ),

    "database": os.getenv(
        "DATABASE_NAME",
        "ai_news",
    ),

    "user": os.getenv(
        "DATABASE_USER",
        "postgres",
    ),

    "password": os.getenv(
        "DATABASE_PASSWORD",
        "root",
    ),
}


BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


# ============================================================
# OLLAMA AI
# ============================================================

OLLAMA_LOCAL_MODEL = os.getenv(
    "OLLAMA_LOCAL_MODEL",
    "qwen3:4b",
)


OLLAMA_CLOUD_MODEL = os.getenv(
    "OLLAMA_CLOUD_MODEL",
    "gpt-oss:20b-cloud",
)


OLLAMA_LOCAL_TIMEOUT = int(
    os.getenv(
        "OLLAMA_LOCAL_TIMEOUT",
        "3",
    )
)


OLLAMA_CLOUD_TIMEOUT = int(
    os.getenv(
        "OLLAMA_CLOUD_TIMEOUT",
        "30",
    )
)