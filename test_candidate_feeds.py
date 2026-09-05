import feedparser


CANDIDATES = [
    {
        "name": "The Guardian World",
        "url": "https://www.theguardian.com/world/rss",
    },
    {
        "name": "Deutsche Welle",
        "url": "https://rss.dw.com/rdf/rss-en-all",
    },
    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
    },
    {
        "name": "Times of India World",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    },
]


def test():

    print()
    print("=" * 60)
    print("CANDIDATE RSS FEEDS")
    print("=" * 60)

    for source in CANDIDATES:

        print()
        print(f"Testing: {source['name']}")
        print(f"URL:     {source['url']}")

        try:

            feed = feedparser.parse(
                source["url"]
            )

            if feed.bozo and not feed.entries:

                print("❌ FAILED")
                print(
                    f"Reason: {feed.bozo_exception}"
                )

                continue

            if not feed.entries:

                print("⚠️ NO ARTICLES")

                continue

            print("✅ HEALTHY")
            print(
                f"Articles: {len(feed.entries)}"
            )

            print(
                "Feed title:",
                feed.feed.get(
                    "title",
                    "Unknown"
                )
            )

        except Exception as exc:

            print("❌ ERROR")
            print(f"Reason: {exc}")


if __name__ == "__main__":
    test()