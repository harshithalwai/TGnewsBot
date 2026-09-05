from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.session import SessionLocal
from models.news import News


class NewsRepository:

    def get_by_title_hash(
        self,
        title_hash: str,
    ):

        with SessionLocal() as session:

            stmt = select(
                News
            ).where(
                News.title_hash == title_hash
            )

            return session.scalar(stmt)


    def exists(
        self,
        hash_value: str,
    ):

        return (
            self.get_by_hash(hash_value)
            is not None
        )


    def mark_posted(
        self,
        news_id: int,
    ):

        with SessionLocal() as session:

            news = session.get(
                News,
                news_id,
            )

            if news:

                news.is_posted = True

                session.commit()


    def get_unposted(
        self,
        limit=None,
    ):

        with SessionLocal() as session:

            stmt = (
                select(News)
                .options(
                    joinedload(News.source)
                )
                .where(
                    News.is_posted == False
                )
                .order_by(
                    News.created_at
                )
            )

            if limit is not None:

                stmt = stmt.limit(
                    limit
                )

            return session.scalars(
                stmt
            ).unique().all()


    def get_by_hash(
        self,
        hash_value: str,
    ):

        with SessionLocal() as session:

            stmt = select(
                News
            ).where(
                News.hash == hash_value
            )

            return session.scalar(stmt)


    def create(
        self,
        **kwargs,
    ):

        with SessionLocal() as session:

            news = News(
                **kwargs
            )

            session.add(news)

            session.commit()

            session.refresh(news)

            return news