import feedparser

from repositories.news_repository import NewsRepository
from repositories.source_repository import SourceRepository
from utils.hash_util import HashUtil


class RSSService:

    BBC_URL = "https://feeds.bbci.co.uk/news/rss.xml"

    def __init__(self):

        self.news_repo = NewsRepository()
        self.source_repo = SourceRepository()

    def fetch(self):

        source = self.source_repo.get_or_create(
            "BBC",
            self.BBC_URL,
        )

        feed = feedparser.parse(self.BBC_URL)

        count = 0

        for article in feed.entries:

            hash_value = HashUtil.generate(
                article.link
            )

            if self.news_repo.exists(hash_value):
                continue

            self.news_repo.create(
                title=article.title,
                summary=None,
                url=article.link,
                image_url=None,
                ai_image=None,
                published_at=None,
                category=None,
                hash=hash_value,
                is_posted=False,
                source_id=source.id,
            )

            count += 1

        return count