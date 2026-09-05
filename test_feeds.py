import feedparser

from services.news.source_manager import SourceManager


def test_feeds():

    sources = SourceManager().get_active_sources()

    print()
    print("=" * 60)
    print("RSS FEED HEALTH CHECK")
    print("=" * 60)

    healthy = 0
    failed = 0

    for source in sources:

        print()
        print(f"Testing: {source.name}")
        print(f"URL:     {source.url}")

        try:

            feed = feedparser.parse(source.url)

            if feed.bozo and not feed.entries:
                print("❌ FAILED")
                print(f"Reason: {feed.bozo_exception}")
                failed += 1
                continue

            if not feed.entries:
                print("⚠️ NO ARTICLES")
                failed += 1
                continue

            print("✅ HEALTHY")
            print(f"Articles available: {len(feed.entries)}")

            if hasattr(feed, "feed"):
                print(
                    f"Feed title: "
                    f"{feed.feed.get('title', 'Unknown')}"
                )

            healthy += 1

        except Exception as exc:

            print("❌ ERROR")
            print(f"Reason: {exc}")

            failed += 1

    print()
    print("=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Healthy feeds : {healthy}")
    print(f"Failed feeds  : {failed}")
    print(f"Total feeds   : {len(sources)}")
    print("=" * 60)


if __name__ == "__main__":
    test_feeds()