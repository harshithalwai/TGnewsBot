from repositories.source_repository import SourceRepository


SOURCES = [

    # ============================================================
    # GLOBAL / WORLD
    # ============================================================

    {
        "name": "BBC News",
        "url": "https://feeds.bbci.co.uk/news/rss.xml",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 10,
    },

    {
        "name": "BBC World",
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 10,
    },

    {
        "name": "The Guardian World",
        "url": "https://www.theguardian.com/world/rss",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Al Jazeera",
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "category": "world",
        "country": "Qatar",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "DW News",
        "url": "https://rss.dw.com/rdf/rss-en-all",
        "category": "world",
        "country": "Germany",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "DW World",
        "url": "https://rss.dw.com/rdf/rss-en-world",
        "category": "world",
        "country": "Germany",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "France 24",
        "url": "https://www.france24.com/en/rss",
        "category": "world",
        "country": "France",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Euronews",
        "url": "https://www.euronews.com/rss?format=mrss&level=theme&name=news",
        "category": "world",
        "country": "Europe",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Sky News World",
        "url": "https://feeds.skynews.com/feeds/rss/world.xml",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Sky News",
        "url": "https://feeds.skynews.com/feeds/rss/home.xml",
        "category": "world",
        "country": "UK",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NPR News",
        "url": "https://feeds.npr.org/1001/rss.xml",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NPR World",
        "url": "https://feeds.npr.org/1004/rss.xml",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "PBS NewsHour",
        "url": "https://www.pbs.org/newshour/feeds/rss/headlines",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "CBC World",
        "url": "https://www.cbc.ca/webfeed/rss/rss-world",
        "category": "world",
        "country": "Canada",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "NHK World",
        "url": "https://www3.nhk.or.jp/rss/news/cat0.xml",
        "category": "world",
        "country": "Japan",
        "language": "English",
        "priority": 7,
    },


    # ============================================================
    # UNITED STATES
    # ============================================================

    {
        "name": "CNN",
        "url": "http://rss.cnn.com/rss/edition.rss",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NBC News",
        "url": "https://feeds.nbcnews.com/nbcnews/public/news",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "CBS News",
        "url": "https://www.cbsnews.com/latest/rss/main",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "New York Times World",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "New York Times",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "category": "world",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },


    # ============================================================
    # INDIA
    # ============================================================

    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/feeder/default.rss",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 10,
    },

    {
        "name": "Indian Express",
        "url": "https://indianexpress.com/feed/",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 10,
    },

    {
        "name": "NDTV",
        "url": "https://feeds.feedburner.com/ndtvnews-top-stories",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Hindustan Times",
        "url": "https://www.hindustantimes.com/feeds/rss/topnews/rssfeed.xml",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Hindustan Times India",
        "url": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Times of India",
        "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Times of India India",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "India Today",
        "url": "https://www.indiatoday.in/rss/home",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "ThePrint",
        "url": "https://theprint.in/feed/",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "The New Indian Express",
        "url": "https://www.newindianexpress.com/feed/",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Deccan Herald",
        "url": "https://www.deccanherald.com/rss-feed",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "The Tribune India",
        "url": "https://www.tribuneindia.com/rss/feed",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "The Week India",
        "url": "https://www.theweek.in/rss",
        "category": "India",
        "country": "India",
        "language": "English",
        "priority": 7,
    },


    # ============================================================
    # BUSINESS / ECONOMICS
    # ============================================================

    {
        "name": "BBC Business",
        "url": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "category": "business",
        "country": "UK",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Guardian Business",
        "url": "https://www.theguardian.com/uk/business/rss",
        "category": "business",
        "country": "UK",
        "language": "English",
        "priority": 7,
    },

    {
        "name": "Hindustan Times Business",
        "url": "https://www.hindustantimes.com/feeds/rss/business/rssfeed.xml",
        "category": "business",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Times of India Business",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
        "category": "business",
        "country": "India",
        "language": "English",
        "priority": 8,
    },


    # ============================================================
    # TECHNOLOGY
    # ============================================================

    {
        "name": "BBC Technology",
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "category": "technology",
        "country": "UK",
        "language": "English",
        "priority": 9,
    },

    {
        "name": "Hindustan Times Technology",
        "url": "https://www.hindustantimes.com/feeds/rss/technology/rssfeed.xml",
        "category": "technology",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Indian Express Technology",
        "url": "https://indianexpress.com/section/technology/feed/",
        "category": "technology",
        "country": "India",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "Indian Express AI",
        "url": "https://indianexpress.com/section/technology/artificial-intelligence/feed/",
        "category": "AI",
        "country": "India",
        "language": "English",
        "priority": 9,
    },


    # ============================================================
    # SCIENCE
    # ============================================================

    {
        "name": "BBC Science",
        "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "category": "science",
        "country": "UK",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NASA News",
        "url": "https://www.nasa.gov/feed/",
        "category": "science",
        "country": "USA",
        "language": "English",
        "priority": 10,
    },

    {
        "name": "NASA Technology",
        "url": "https://www.nasa.gov/technology/feed/",
        "category": "technology",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "NASA Artemis",
        "url": "https://www.nasa.gov/humans-in-space/artemis/feed/",
        "category": "space",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },

    {
        "name": "JPL News",
        "url": "https://www.jpl.nasa.gov/feeds/news/",
        "category": "space",
        "country": "USA",
        "language": "English",
        "priority": 8,
    },


    # ============================================================
    # SPACE
    # ============================================================

    {
        "name": "Space.com",
        "url": "https://www.space.com/feeds/all",
        "category": "space",
        "country": "USA",
        "language": "English",
        "priority": 7,
    },


    # ============================================================
    # SPORTS
    # ============================================================

    {
        "name": "BBC Sport",
        "url": "https://feeds.bbci.co.uk/sport/rss.xml",
        "category": "sports",
        "country": "UK",
        "language": "English",
        "priority": 6,
    },

    {
        "name": "Hindustan Times Sports",
        "url": "https://www.hindustantimes.com/feeds/rss/sports/rssfeed.xml",
        "category": "sports",
        "country": "India",
        "language": "English",
        "priority": 6,
    },

    {
        "name": "Times of India Sports",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
        "category": "sports",
        "country": "India",
        "language": "English",
        "priority": 6,
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
            source_type="rss",
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
    print("=" * 60)
    print(f"Sources added: {added}")
    print(f"Sources already existed: {existing}")
    print(f"Total configured: {len(SOURCES)}")
    print("=" * 60)


if __name__ == "__main__":
    seed_sources()