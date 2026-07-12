                   AI NEWS AGENT

                +-------------------+
                |   APScheduler     |
                +---------+---------+
                          |
                          |
                          ▼
                +-------------------+
                |  News Collector   |
                | (RSS Feeds)       |
                +---------+---------+
                          |
                          ▼
                +-------------------+
                | PostgreSQL        |
                | Raw News Storage  |
                +---------+---------+
                          |
                          ▼
                +-------------------+
                | Duplicate Checker |
                +---------+---------+
                          |
                          ▼
                +-------------------+
                | AI Summarizer     |
                | (Ollama)          |
                +---------+---------+
                          |
                          ▼
                +-------------------+
                | AI Image Creator  |
                | (FLUX)            |
                +---------+---------+
                          |
                          ▼
                +-------------------+
                | Telegram Sender   |
                +---------+---------+
                          |
                          ▼
                     Telegram Groups




## Folder Structure 

AI-News-Agent/

│
├── app/
│
├── config/
│
├── database/
│
├── models/
│
├── repositories/
│
├── services/
│
├── telegram/
│
├── scheduler/
│
├── prompts/
│
├── images/
│
├── logs/
│
├── tests/
│
├── .env
│
├── requirements.txt
│
├── main.py
│
└── README.md


## virtual env

1. python -m venv .venv
-- if any issue occure  - Remove-Item -Recurse -Force .venv
2. .venv\Scripts\Activate

## install the required packages 

pip install sqlalchemy psycopg2-binary python-dotenv loguru
pip freeze > requirements.txt

## Step 2 — Create These Files

Inside your project:

config/

    __init__.py

    settings.py

database/

    __init__.py

    db.py

main.py


## Our Database Design 

We will use 5 tables.

news
sources
telegram_groups
posted_news
settings

Why separate tables?

News
│
├── comes from Source
│
├── sent to Telegram Groups
│
└── tracked in Posted News




## Final Architecture

AI-News-Agent/

├── alembic/
├── config/
├── database/
├── models/
├── repositories/
├── services/
│   ├── rss/
│   ├── ai/
│   ├── telegram/
│   ├── image/
│   └── scheduler/
├── prompts/
├── logs/
├── images/
├── tests/
├── .env
├── main.py
└── requirements.txt