from services.scheduler.scheduler_service import (
    SchedulerService,
)

from services.telegram.telegram_bot import (
    TelegramBot,
)


def main():

    print()
    print("=" * 60)
    print("AI NEWS BOT STARTING")
    print("=" * 60)

    # ============================================================
    # CREATE SCHEDULER
    # ============================================================

    scheduler_service = (
        SchedulerService()
    )

    # ============================================================
    # START NEWS AUTOMATICALLY
    # ============================================================

    scheduler_service.start_news(
        run_immediately=True
    )

    # ============================================================
    # START TELEGRAM BOT
    # ============================================================

    bot = TelegramBot(
        scheduler_service
    )

    bot.run()


if __name__ == "__main__":

    main()