from datetime import datetime

from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from pipeline.news_pipeline import NewsPipeline


class SchedulerService:

    def __init__(self):

        self.scheduler = (
            BackgroundScheduler()
        )

        self.pipeline = (
            NewsPipeline()
        )

        self.is_running = False

    # ============================================================
    # START
    # ============================================================

    def start_news(
        self,
        run_immediately=True,
    ):

        # Already running
        if self.scheduler.get_job(
            "news_pipeline"
        ):

            self.is_running = True

            return False

        self.scheduler.add_job(

            self.pipeline.run,

            trigger="interval",

            minutes=1,

            id="news_pipeline",

            replace_existing=True,

            max_instances=1,

            coalesce=True,

            misfire_grace_time=30,

            next_run_time=(
                datetime.now()
                if run_immediately
                else None
            ),
        )

        if not self.scheduler.running:

            self.scheduler.start()

        self.is_running = True

        print()
        print("=" * 60)
        print("NEWS PIPELINE STARTED")
        print("=" * 60)
        print("Interval: 1 minute")
        print("Maximum concurrent pipelines: 1")
        print("Initial run: IMMEDIATE")
        print("=" * 60)

        return True

    # ============================================================
    # STOP
    # ============================================================

    def stop_news(self):

        job = self.scheduler.get_job(
            "news_pipeline"
        )

        if not job:

            self.is_running = False

            return False

        self.scheduler.remove_job(
            "news_pipeline"
        )

        self.is_running = False

        print()
        print("=" * 60)
        print("NEWS PIPELINE STOPPED")
        print("=" * 60)

        return True

    # ============================================================
    # STATUS
    # ============================================================

    def get_status(self):

        return (
            self.scheduler.get_job(
                "news_pipeline"
            )
            is not None
        )

    # ============================================================
    # RUN NOW
    # ============================================================

    def run_now(self):

        print()
        print("Running news pipeline manually...")

        self.pipeline.run()

        return True

    # ============================================================
    # START PROGRAM
    # ============================================================

    def start(self):

        return self.start_news(
            run_immediately=True
        )