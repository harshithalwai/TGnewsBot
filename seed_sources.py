from repositories.source_repository import SourceRepository


SOURCES = [

    # =========================
    # WORLD / GENERAL
    # =========================

    {
        "name": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
        "source_type": "rss",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 10,
    },

    # =========================
    # SCIENCE / SPACE
    # =========================

    {
        "name": "NASA News",
        "url": "https://www.nasa.gov/feed/",
        "source_type": "rss",
        "category": "science",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NASA Technology",
        "url": "https://www.nasa.gov/technology/feed/",
        "source_type": "rss",
        "category": "technology",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "NASA Artemis",
        "url": "https://www.nasa.gov/humans-in-space/artemis/feed/",
        "source_type": "rss",
        "category": "space",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "JPL News",
        "url": "https://www.jpl.nasa.gov/feeds/news/",
        "source_type": "rss",
        "category": "space",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },
    # =========================
    # WORLD NEWS
    # =========================

    {
        "name": "The Guardian World",
        "url": "https://www.theguardian.com/world/rss",
        "source_type": "rss",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Deutsche Welle",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "source_type": "rss",
        "category": "world",
        "country": "Germany",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "source_type": "rss",
        "category": "world",
        "country": "Qatar",
        "language": "English",
        "priority": 8,
    },

    # =========================
    # INDIA
    # =========================

    {
        "name": "Times of India World",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
        "source_type": "rss",
        "category": "india",
        "country": "India",
        "language": "English",
        "priority": 8,
    },
]


def seed_sources():

    repository = SourceRepository()

    added = 0
    existing = 0

    for data in SOURCES:

        source = repository.get_by_name(
            data["name"]
        )

        if source:

            print(
                f"EXISTS: {source.name}"
            )

            existing += 1

            continue

        repository.get_or_create(
            name=data["name"],
            url=data["url"],
            source_type=data["source_type"],
            category=data["category"],
            country=data["country"],
            language=data["language"],
            priority=data["priority"],
        )

        print(
            f"ADDED: {data['name']}"
        )

        added += 1

    print()
    print(f"Sources added: {added}")
    print(f"Sources already existed: {existing}")


if __name__ == "__main__":
    seed_sources()