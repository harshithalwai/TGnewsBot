from apscheduler.schedulers.blocking import BlockingScheduler

from pipeline.news_pipeline import NewsPipeline
from services.news.rss_collector import RSSCollector


class SchedulerService:

    def __init__(self):

        self.scheduler = BlockingScheduler()

        self.rss_collector = RSSCollector()

        self.pipeline = NewsPipeline()


    # ============================================================
    # MAIN JOB
    # ============================================================

    def run_job(self):

        print()
        print("=" * 60)
        print("SCHEDULED NEWS JOB")
        print("=" * 60)


        # ========================================================
        # 1. COLLECT RSS
        # ========================================================

        print()
        print("Collecting RSS news...")

        try:

            new_articles = (
                self.rss_collector.collect_all()
            )

            print(
                f"RSS collection complete. "
                f"New articles: {new_articles}"
            )

        except Exception as exc:

            print(
                f"RSS collection failed: {exc}"
            )

            new_articles = 0


        # ========================================================
        # 2. PROCESS ONE NEWS
        # ========================================================

        print()
        print("Running AI + Telegram pipeline...")

        try:

            self.pipeline.run()

        except Exception as exc:

            print(
                f"Pipeline failed: {exc}"
            )


        print()
        print("=" * 60)
        print("SCHEDULED NEWS JOB FINISHED")
        print("=" * 60)


    # ============================================================
    # START
    # ============================================================

    def start(self):

        print()
        print("=" * 60)
        print("AI NEWS BOT")
        print("=" * 60)

        print(
            "Scheduler Started..."
        )

        print(
            "Interval: 30 seconds"
        )


        # --------------------------------------------------------
        # Run immediately
        # --------------------------------------------------------

        self.run_job()


        # --------------------------------------------------------
        # Schedule
        # --------------------------------------------------------

        self.scheduler.add_job(

            self.run_job,

            trigger="interval",

            seconds=30,

            id="news_pipeline",

            replace_existing=True,

            max_instances=1,

            coalesce=True,
        )


        try:

            self.scheduler.start()

        except (KeyboardInterrupt, SystemExit):

            print(
                "\nScheduler stopped."
            )