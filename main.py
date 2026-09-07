from services.scheduler.scheduler_service import SchedulerService
from services.telegram.telegram_bot import TelegramBot


def main():

    print()
    print("=" * 60)
    print("AI TELEGRAM NEWS BOT")
    print("=" * 60)


    # ============================================================
    # CREATE SCHEDULER
    # ============================================================

    scheduler = SchedulerService()


    # ============================================================
    # START NEWS SYSTEM
    # ============================================================

    scheduler.start()


    # ============================================================
    # START TELEGRAM BOT
    # ============================================================

    telegram_bot = TelegramBot(
        scheduler_service=scheduler
    )


    telegram_bot.run()


if __name__ == "__main__":

    main()