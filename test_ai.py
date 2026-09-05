from repositories.news_repository import NewsRepository
from repositories.telegram_group_repository import TelegramGroupRepository

from services.telegram.telegram_service import TelegramService
from pipeline.news_pipeline import NewsPipeline


def main():

    print("=" * 60)
    print("TESTING AI + TELEGRAM")
    print("=" * 60)

    news_repo = NewsRepository()
    group_repo = TelegramGroupRepository()
    telegram = TelegramService()
    pipeline = NewsPipeline()

    # ============================================================
    # GET ONE UNPOSTED NEWS
    # ============================================================

    news_list = news_repo.get_unposted()

    if not news_list:

        print()
        print("NO UNPOSTED NEWS")
        return

    news = news_list[0]

    print()
    print("NEWS ID:", news.id)
    print("TITLE:", news.title)

    print(
        "SOURCE:",
        news.source.name if news.source else "Unknown"
    )

    # ============================================================
    # GENERATE AI
    # ============================================================

    print()
    print("Generating AI content...")

    try:

        result = pipeline.ai.generate(

            title=news.title,

            article=(
                news.summary
                or news.title
            ),

            source=(
                news.source.name
                if news.source
                else "Unknown"
            ),
        )

    except Exception as exc:

        print()
        print("AI FAILED")
        print("ERROR:", exc)

        return

    print("AI generation successful.")

    # ============================================================
    # BUILD TELEGRAM MESSAGE
    # ============================================================

    message = pipeline.build_message(
        news,
        result,
    )

    print()
    print("=" * 60)
    print("TELEGRAM MESSAGE")
    print("=" * 60)

    print(message)

    # ============================================================
    # GET GROUPS
    # ============================================================

    groups = group_repo.get_active()

    print()
    print(
        f"Active groups: {len(groups)}"
    )

    if not groups:

        print()
        print("NO ACTIVE TELEGRAM GROUPS")
        return

    # ============================================================
    # SEND
    # ============================================================

    for group in groups:

        print()
        print(
            f"Sending to: {group.title}"
        )

        try:

            telegram.send_message(
                group.chat_id,
                message,
            )

            print(
                f"Sent successfully to "
                f"{group.title}"
            )

        except Exception as exc:

            print(
                f"Failed sending to "
                f"{group.title}: {exc}"
            )

    # ============================================================
    # IMPORTANT
    # ============================================================

    print()
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

    print()
    print("IMPORTANT:")
    print("News was NOT marked as posted.")
    print("It can be tested again.")


# ============================================================
# WINDOWS ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()