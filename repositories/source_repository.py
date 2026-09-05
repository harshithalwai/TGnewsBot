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

    def get_active(self):

        with SessionLocal() as session:

            stmt = (
                select(Source)
                .where(Source.is_active == True)
                .order_by(
                    Source.priority.desc(),
                    Source.name
                )
            )

            return session.scalars(stmt).all()

    def get_or_create(
        self,
        name: str,
        url: str,
        source_type: str = "rss",
        category: str | None = None,
        country: str | None = None,
        language: str | None = None,
        priority: int = 5,
    ):

        source = self.get_by_name(name)

        if source:
            return source

        with SessionLocal() as session:

            source = Source(
                name=name,
                url=url,
                source_type=source_type,
                category=category,
                country=country,
                language=language,
                priority=priority,
                is_active=True,
            )

            session.add(source)
            session.commit()
            session.refresh(source)

            return source