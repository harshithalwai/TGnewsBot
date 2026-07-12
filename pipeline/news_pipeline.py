from repositories.news_repository import NewsRepository
from repositories.telegram_group_repository import TelegramGroupRepository
from services.telegram.telegram_service import TelegramService


class NewsPipeline:

    def __init__(self):

        self.news_repo = NewsRepository()
        self.group_repo = TelegramGroupRepository()
        self.telegram = TelegramService()

    def run(self):

        news_list = self.news_repo.get_unposted()

        groups = self.group_repo.get_active()

        print(f"News : {len(news_list)}")
        print(f"Groups : {len(groups)}")

        for news in news_list:

            message = f"""
📰 {news.title}

🔗 {news.url}
"""

            for group in groups:

                self.telegram.send_message(
                    group.chat_id,
                    message,
                )

            self.news_repo.mark_posted(news.id)

        print("Pipeline Finished.")