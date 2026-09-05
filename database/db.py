from sqlalchemy import create_engine

from config.settings import DATABASE


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DATABASE['user']}:"
    f"{DATABASE['password']}@"
    f"{DATABASE['host']}:"
    f"{DATABASE['port']}/"
    f"{DATABASE['database']}"
)


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)