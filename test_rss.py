from services.news.rss_collector import RSSCollector


def main():

    collector = RSSCollector()

    print("=" * 60)
    print("COLLECTING RSS NEWS")
    print("=" * 60)

    count = collector.collect_all()

    print()

    print(
        f"New articles: {count}"
    )


if __name__ == "__main__":

    main()