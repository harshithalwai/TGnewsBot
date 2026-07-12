from sqlalchemy import select
from database.session import SessionLocal
from models.news import News


class NewsRepository:
    def exists(self, hash_value: str):
        return self.get_by_hash(hash_value) is not None
    def mark_posted(self, news_id: int):

        with SessionLocal() as session:

            news = session.get(News, news_id)

            if news:

                news.is_posted = True

                session.commit()
    def get_unposted(self):

        with SessionLocal() as session:

            stmt = (
                select(News)
                .where(News.is_posted == False)
                .order_by(News.created_at)
            )

            return session.scalars(stmt).all()
    def get_by_hash(self, hash_value: str):

        with SessionLocal() as session:

            stmt = select(News).where(
                News.hash == hash_value
            )

            return session.scalar(stmt)

    def create(self, **kwargs):

        with SessionLocal() as session:

            news = News(**kwargs)

            session.add(news)

            session.commit()

            session.refresh(news)

            return news