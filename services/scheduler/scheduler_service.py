from apscheduler.schedulers.blocking import BlockingScheduler

from pipeline.news_pipeline import NewsPipeline


class SchedulerService:

    def __init__(self):

        self.scheduler = BlockingScheduler()

        self.pipeline = NewsPipeline()

    def start(self):

        self.scheduler.add_job(
            self.pipeline.run,
            trigger="interval",
            # minutes=5,
            seconds=30,
            id="news_pipeline",
            replace_existing=True,
        )

        print("Scheduler Started...")

        self.pipeline.run()

        self.scheduler.start()