from sqlalchemy import select

from database.session import SessionLocal
from models.source import Source


class SourceRepository:

    def get_by_name(self, name: str):

        with SessionLocal() as session:

            stmt = select(Source).where(
                Source.name == name
            )

            return session.scalar(stmt)

    def get_or_create(self, name: str, url: str):

        source = self.get_by_name(name)

        if source:
            return source

        with SessionLocal() as session:

            source = Source(
                name=name,
                url=url,
            )

            session.add(source)

            session.commit()

            session.refresh(source)

            return source