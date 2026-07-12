from sqlalchemy.orm import sessionmaker

from database.db import engine

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)