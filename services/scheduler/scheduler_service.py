from apscheduler.schedulers.blocking import BlockingScheduler

from pipeline.news_pipeline import NewsPipeline
from services.telegram.telegram_discovery import (
    TelegramDiscoveryService,
)


class SchedulerService:

    def __init__(self):

        self.scheduler = BlockingScheduler()

        self.pipeline = NewsPipeline()

        self.telegram_discovery = (
            TelegramDiscoveryService()
        )

    # ============================================================
    # START
    # ============================================================

    def start(self):

        # ========================================================
        # START TELEGRAM AUTO DISCOVERY
        # ========================================================

        print()
        print("=" * 60)
        print(
            "STARTING TELEGRAM AUTO DISCOVERY"
        )
        print("=" * 60)

        self.telegram_discovery.start()

        print(
            "Telegram group/channel discovery: ENABLED"
        )

        # ========================================================
        # NEWS PIPELINE
        # ========================================================

        self.scheduler.add_job(

            self.pipeline.run,

            trigger="interval",

            minutes=1,

            id="news_pipeline",

            replace_existing=True,

            max_instances=1,

            coalesce=True,

            misfire_grace_time=30,
        )

        # ========================================================
        # STARTUP INFORMATION
        # ========================================================

        print()
        print("=" * 60)
        print("NEWS SCHEDULER STARTED")
        print("=" * 60)

        print(
            "Pipeline interval: 1 minute"
        )

        print(
            "Maximum concurrent pipelines: 1"
        )

        print(
            "Telegram auto-discovery: ENABLED"
        )

        print("=" * 60)

        # ========================================================
        # RUN IMMEDIATELY
        # ========================================================

        print()
        print(
            "Running initial pipeline..."
        )

        try:

            self.pipeline.run()

        except Exception as exc:

            print(
                f"Initial pipeline failed: {exc}"
            )

        # ========================================================
        # START SCHEDULER
        # ========================================================

        print()
        print(
            "Waiting for next scheduled run..."
        )

        print(
            "Next pipeline run: approximately 1 minute"
        )

        print()

        try:

            self.scheduler.start()

        except (
            KeyboardInterrupt,
            SystemExit,
        ):

            print()
            print(
                "Stopping services..."
            )

            self.telegram_discovery.stop()

            self.scheduler.shutdown(
                wait=False
            )