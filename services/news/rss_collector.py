import feedparser
import requests

from datetime import timezone
from email.utils import parsedate_to_datetime

from loguru import logger

from repositories.news_repository import NewsRepository
from repositories.source_repository import SourceRepository
from utils.hash_util import HashUtil


class RSSCollector:

    REQUEST_TIMEOUT = 10

    USER_AGENT = (
        "AI-News-Agent/1.0 "
        "(RSS news aggregation)"
    )

    def __init__(self):

        self.news_repo = NewsRepository()

        self.source_repo = (
            SourceRepository()
        )

    # ============================================================
    # PUBLISHED DATE
    # ============================================================

    @staticmethod
    def extract_published_at(article):

        published = getattr(
            article,
            "published",
            None,
        )

        if not published:

            published = getattr(
                article,
                "updated",
                None,
            )

        if not published:

            return None

        try:

            dt = parsedate_to_datetime(
                published
            )

            if dt.tzinfo is not None:

                dt = dt.astimezone(
                    timezone.utc
                ).replace(
                    tzinfo=None
                )

            return dt

        except (
            TypeError,
            ValueError,
            OverflowError,
        ):

            return None

    # ============================================================
    # IMAGE
    # ============================================================

    @staticmethod
    def extract_image_url(article):

        media_thumbnail = getattr(
            article,
            "media_thumbnail",
            None,
        )

        if media_thumbnail:

            url = media_thumbnail[0].get(
                "url"
            )

            if url:

                return url

        for media in getattr(
            article,
            "media_content",
            [],
        ):

            url = media.get("url")

            if url:

                return url

        for enclosure in getattr(
            article,
            "enclosures",
            [],
        ):

            url = enclosure.get("href")

            if url:

                return url

        return None

    # ============================================================
    # FETCH
    # ============================================================

    def fetch_feed(self, url):

        response = requests.get(
            url,
            timeout=self.REQUEST_TIMEOUT,
            headers={
                "User-Agent": self.USER_AGENT
            },
        )

        response.raise_for_status()

        feed = feedparser.parse(
            response.content
        )

        if feed.bozo and not feed.entries:

            raise RuntimeError(
                "Invalid RSS/Atom feed"
            )

        if not feed.entries:

            raise RuntimeError(
                "Feed contains no articles"
            )

        return feed

    # ============================================================
    # COLLECT ONE SOURCE
    # ============================================================

    def collect(self, source):

        logger.info(
            f"Fetching RSS: "
            f"{source.name} -> {source.url}"
        )

        feed = self.fetch_feed(
            source.url
        )

        count = 0

        for article in feed.entries:

            url = getattr(
                article,
                "link",
                None,
            )

            title = getattr(
                article,
                "title",
                None,
            )

            if not url or not title:

                continue

            hash_value = (
                HashUtil.generate(url)
            )

            title_hash = (
                HashUtil.generate_title_hash(
                    title
                )
            )

            # URL duplicate
            if self.news_repo.exists(
                hash_value
            ):

                continue

            # Title duplicate
            if self.news_repo.get_by_title_hash(
                title_hash
            ):

                logger.debug(
                    f"Duplicate title skipped: "
                    f"{title}"
                )

                continue

            summary = getattr(
                article,
                "summary",
                None,
            )

            published_at = (
                self.extract_published_at(
                    article
                )
            )

            image_url = (
                self.extract_image_url(
                    article
                )
            )

            self.news_repo.create(

                title=title,

                summary=summary,

                url=url,

                image_url=image_url,

                ai_image=None,

                published_at=published_at,

                category=source.category,

                hash=hash_value,

                is_posted=False,

                title_hash=title_hash,

                source_id=source.id,
            )

            count += 1

        logger.info(
            f"{source.name}: "
            f"{count} new articles"
        )

        return count

    # ============================================================
    # COLLECT ALL
    # ============================================================

    def collect_all(self):

        sources = (
            self.source_repo.get_active()
        )

        total = 0

        for source in sources:

            if (
                source.source_type.lower()
                != "rss"
            ):

                continue

            try:

                total += self.collect(
                    source
                )

            except requests.RequestException as exc:

                logger.error(
                    f"RSS request failed for "
                    f"{source.name}: {exc}"
                )

            except Exception as exc:

                logger.exception(
                    f"RSS collection failed for "
                    f"{source.name}: {exc}"
                )

        logger.info(
            f"RSS collection completed. "
            f"Total new articles: {total}"
        )

        return total