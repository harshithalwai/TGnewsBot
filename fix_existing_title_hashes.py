from database.session import SessionLocal
from models.news import News
from utils.hash_util import HashUtil


def main():

    with SessionLocal() as session:

        news_list = session.query(News).all()

        updated = 0

        for news in news_list:

            news.title_hash = (
                HashUtil.generate_title_hash(
                    news.title
                )
            )

            updated += 1

        session.commit()

        print(
            f"Updated title hashes: {updated}"
        )


if __name__ == "__main__":
    main()