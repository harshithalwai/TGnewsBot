from repositories.news_repository import NewsRepository
from repositories.telegram_group_repository import TelegramGroupRepository

from services.news.article_extractor import ArticleExtractor
from services.news.rss_collector import RSSCollector

from services.telegram.telegram_service import TelegramService
from services.ai.ollama_service import OllamaService


class NewsPipeline:

    def __init__(self):

        self.news_repo = NewsRepository()

        self.group_repo = (
            TelegramGroupRepository()
        )

        self.telegram = TelegramService()

        self.ai = OllamaService()

        # RSS collector
        self.rss = RSSCollector()

        # Article extractor
        self.article_extractor = ArticleExtractor()


    # ============================================================
    # BUILD TELEGRAM MESSAGE
    # ============================================================

    def build_message(
        self,
        news,
        ai_result,
    ):

        message = (
            f"📰 <b>{ai_result.headline or news.title}</b>\n\n"
        )

        message += (
            f"📂 <b>Category:</b> "
            f"{ai_result.category or 'General'}\n\n"
        )


        # ========================================================
        # SUMMARY
        # ========================================================

        message += (
            "📝 <b>Summary</b>\n"
            f"{ai_result.summary or news.summary or 'No summary available.'}\n"
        )


        # ========================================================
        # HIGHLIGHTS
        # ========================================================

        if ai_result.highlights:

            message += (
                "\n\n🔹 <b>Key Highlights</b>\n"
            )

            for item in ai_result.highlights:

                message += (
                    f"• {item}\n"
                )


        # ========================================================
        # ANALYSIS SECTIONS
        # ========================================================

        if ai_result.sections:

            message += (
                "\n📚 <b>Analysis</b>\n"
            )

            for section in ai_result.sections:

                message += (
                    f"• {section}\n"
                )


        # ========================================================
        # AI EXPLAINS
        # ========================================================

        if ai_result.ai_explains:

            message += (
                "\n💡 <b>AI Explains</b>\n"
                f"{ai_result.ai_explains}\n"
            )


        # ========================================================
        # EXAM NOTES
        # ========================================================

        if ai_result.exam_notes:

            message += (
                "\n🎓 <b>Exam Notes</b>\n"
            )

            for item in ai_result.exam_notes:

                message += (
                    f"• {item}\n"
                )


        # ========================================================
        # INTERVIEW QUESTION
        # ========================================================

        if ai_result.interview_question:

            question = ai_result.interview_question


            if question.question:

                message += (
                    "\n🎤 <b>Interview Question</b>\n"
                    f"{question.question}\n"
                )


            if question.answer:

                message += (
                    f"<b>Answer:</b> "
                    f"{question.answer}\n"
                )


        # ========================================================
        # IMPORTANT TERMS
        # ========================================================

        if ai_result.important_terms:

            message += (
                "\n🔑 <b>Important Terms</b>\n"
            )

            for term in ai_result.important_terms:

                message += (
                    f"• {term}\n"
                )


        # ========================================================
        # RECOMMENDATIONS
        # ========================================================

        if ai_result.recommendations:

            message += (
                "\n✅ <b>Recommendations</b>\n"
            )

            for recommendation in ai_result.recommendations:

                message += (
                    f"• {recommendation}\n"
                )


        # ========================================================
        # HASHTAGS
        # ========================================================

        if ai_result.hashtags:

            message += (
                "\n"
                + " ".join(ai_result.hashtags)
            )


        # ========================================================
        # SOURCE
        # ========================================================

        source_name = (
            news.source.name
            if news.source
            else "Unknown"
        )

        message += (
            "\n\n"
            f"🔗 <b>Source:</b> {source_name}\n"
            f"🌐 {news.url}"
        )


        return message


    # ============================================================
    # PROCESS ONE NEWS ARTICLE
    # ============================================================

    def process_news(
        self,
        news,
        groups,
    ):

        print()
        print("=" * 60)
        print(
            f"Processing news ID: {news.id}"
        )
        print(
            f"Title: {news.title}"
        )
        print(
            f"Source: "
            f"{news.source.name if news.source else 'Unknown'}"
        )
        print("=" * 60)


        # ========================================================
        # 1. EXTRACT ARTICLE
        # ========================================================

        print()
        print(
            "Extracting article content..."
        )


        article_text = (
            self.article_extractor.extract(
                news.url
            )
        )


        # --------------------------------------------------------
        # FALLBACK
        # --------------------------------------------------------

        if not article_text:

            print(
                "Article extraction failed."
            )

            print(
                "Using RSS summary/title as fallback."
            )

            article_text = (
                news.summary
                or news.title
            )

        else:

            print(
                "Article extraction successful."
            )


        print(
            f"Article content length: "
            f"{len(article_text)} characters"
        )


        # ========================================================
        # 2. AI GENERATION
        # ========================================================

        print()
        print(
            "Generating AI content..."
        )


        ai_result = self.ai.generate(

            title=news.title,

            article=article_text,

            source=(
                news.source.name
                if news.source
                else "Unknown"
            ),
        )


        print(
            "AI generation successful."
        )


        # ========================================================
        # 3. BUILD TELEGRAM MESSAGE
        # ========================================================

        message = self.build_message(
            news,
            ai_result,
        )


        print()
        print(
            "Generated Telegram message:"
        )
        print("-" * 60)

        print(message)

        print("-" * 60)


        # ========================================================
        # 4. SEND TO TELEGRAM
        # ========================================================

        sent_successfully = True


        for group in groups:

            print()
            print(
                f"Sending to: {group.title}"
            )


            try:

                self.telegram.send_message(
                    group.chat_id,
                    message,
                )


                print(
                    f"Sent successfully to "
                    f"{group.title}"
                )


            except Exception as exc:

                sent_successfully = False


                print(
                    f"Telegram failed for "
                    f"{group.title}: {exc}"
                )


        # ========================================================
        # 5. MARK POSTED
        # ========================================================

        if sent_successfully:

            self.news_repo.mark_posted(
                news.id
            )


            print()
            print(
                f"News {news.id} "
                f"marked as posted."
            )


            return True


        print()
        print(
            f"News {news.id} "
            f"NOT marked as posted."
        )

        return False


    # ============================================================
    # RUN PIPELINE
    # ============================================================

    def run(self):

        print()
        print("=" * 60)
        print(
            "NEWS PIPELINE STARTED"
        )
        print("=" * 60)


        # ========================================================
        # 1. COLLECT RSS
        # ========================================================

        print()
        print(
            "Collecting latest RSS news..."
        )


        try:

            new_articles = (
                self.rss.collect_all()
            )


            print(
                f"New RSS articles collected: "
                f"{new_articles}"
            )


        except Exception as exc:

            print(
                f"⚠️ RSS collection failed: "
                f"{exc}"
            )


        # ========================================================
        # 2. GET ACTIVE TELEGRAM GROUPS
        # ========================================================

        print()
        print(
            "Loading active Telegram groups..."
        )


        groups = (
            self.group_repo.get_active()
        )


        if not groups:

            print()
            print(
                "❌ No active Telegram groups."
            )

            return


        print(
            f"Active Telegram groups: "
            f"{len(groups)}"
        )


        # ========================================================
        # 3. GET ONE UNPOSTED ARTICLE
        # ========================================================

        print()
        print(
            "Looking for unposted news..."
        )


        news_list = (
            self.news_repo.get_unposted(
                limit=1
            )
        )


        if not news_list:

            print()
            print(
                "No unposted news available."
            )

            print()
            print("=" * 60)
            print(
                "NEWS PIPELINE FINISHED"
            )
            print("=" * 60)

            return


        news = news_list[0]


        print()
        print(
            f"Selected news ID: "
            f"{news.id}"
        )


        # ========================================================
        # 4. PROCESS ARTICLE
        # ========================================================

        try:

            self.process_news(
                news,
                groups,
            )


        except Exception as exc:

            print()
            print(
                f"❌ Failed processing "
                f"news {news.id}: {exc}"
            )

            print(
                "Article remains unposted."
            )


        # ========================================================
        # FINISHED
        # ========================================================

        print()
        print("=" * 60)
        print(
            "NEWS PIPELINE FINISHED"
        )
        print("=" * 60)