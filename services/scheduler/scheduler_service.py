from apscheduler.schedulers.background import BackgroundScheduler

from pipeline.news_pipeline import NewsPipeline


class SchedulerService:

    def __init__(self):

        self.scheduler = BackgroundScheduler()

        self.pipeline = NewsPipeline()

        self.is_running = False


    # ============================================================
    # START NEWS
    # ============================================================

    def start_news(self):

        if self.is_running:

            print("News scheduler is already running.")

            return False


        # --------------------------------------------------------
        # Add job
        # --------------------------------------------------------

        if not self.scheduler.get_job("news_pipeline"):

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


        # --------------------------------------------------------
        # Start scheduler
        # --------------------------------------------------------

        if not self.scheduler.running:

            self.scheduler.start()


        self.is_running = True


        print()
        print("=" * 60)
        print("NEWS POSTING STARTED")
        print("=" * 60)

        print("Pipeline interval: 1 minute")
        print("Maximum concurrent pipelines: 1")

        print("=" * 60)


        return True


    # ============================================================
    # STOP NEWS
    # ============================================================

    def stop_news(self):

        if not self.is_running:

            print("News scheduler is already stopped.")

            return False


        job = self.scheduler.get_job(
            "news_pipeline"
        )


        if job:

            self.scheduler.remove_job(
                "news_pipeline"
            )


        self.is_running = False


        print()
        print("=" * 60)
        print("NEWS POSTING STOPPED")
        print("=" * 60)


        return True


    # ============================================================
    # STATUS
    # ============================================================

    def get_status(self):

        return self.is_running


    # ============================================================
    # RUN PIPELINE IMMEDIATELY
    # ============================================================

    def run_now(self):

        if not self.is_running:

            print(
                "News scheduler is stopped."
            )

            return


        print()
        print(
            "Running news pipeline..."
        )


        self.pipeline.run()


    # ============================================================
    # START PROGRAM
    # ============================================================

    def start(self):

        # --------------------------------------------------------
        # START NEWS AUTOMATICALLY
        # --------------------------------------------------------

        self.start_news()


        # --------------------------------------------------------
        # RUN IMMEDIATELY
        # --------------------------------------------------------

        print()
        print(
            "Running initial pipeline..."
        )


        self.pipeline.run()