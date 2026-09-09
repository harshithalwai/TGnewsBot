from loguru import logger

from services.news.rss_collector import RSSCollector
from services.news.article_extractor import ArticleExtractor

from services.telegram.telegram_service import TelegramService

from repositories.news_repository import NewsRepository
from repositories.telegram_group_repository import (
    TelegramGroupRepository,
)

from services.ai.ollama_service import OllamaService
from services.ai.schemas import (
    AIResponse,
)


class NewsPipeline:

    # ============================================================
    # CONFIGURATION
    # ============================================================

    # Number of articles processed in one pipeline run.
    BATCH_SIZE = 5

    def __init__(self):

        self.news_repo = NewsRepository()

        self.group_repo = (
            TelegramGroupRepository()
        )

        self.collector = RSSCollector()

        self.telegram = TelegramService()

        self.ai = OllamaService()

    # ============================================================
    # RUN
    # ============================================================

    def run(self):

        logger.info(
            "=================================================="
        )

        logger.info(
            "NEWS PIPELINE STARTED"
        )

        # ========================================================
        # STEP 1
        # COLLECT NEWS
        # ========================================================

        try:

            collected = (
                self.collector.collect_all()
            )

            logger.info(
                f"RSS collection added "
                f"{collected} new articles"
            )

        except Exception as exc:

            logger.exception(
                f"RSS collection failed: {exc}"
            )

        # ========================================================
        # STEP 2
        # GET ENABLED TELEGRAM CHATS
        # ========================================================

        groups = (
            self.group_repo
            .get_news_enabled_groups()
        )

        if not groups:

            logger.warning(
                "No Telegram chats have news enabled."
            )

            return

        logger.info(
            f"News enabled chats: {len(groups)}"
        )

        for group in groups:

            logger.info(
                f"Target chat: "
                f"{group.title} | "
                f"{group.chat_id} | "
                f"{group.chat_type}"
            )

        # ========================================================
        # STEP 3
        # GET UNPOSTED ARTICLES
        # ========================================================

        articles = (
            self.news_repo.get_unposted(
                limit=self.BATCH_SIZE
            )
        )

        if not articles:

            logger.info(
                "No unposted articles."
            )

            return

        logger.info(
            f"Processing {len(articles)} articles"
        )

        # ========================================================
        # STEP 4
        # PROCESS ARTICLES
        # ========================================================

        for news in articles:

            try:

                self.process_article(
                    news=news,
                    groups=groups,
                )

            except Exception as exc:

                logger.exception(
                    f"Article processing failed: "
                    f"{news.title} | {exc}"
                )

        logger.info(
            "NEWS PIPELINE FINISHED"
        )

    # ============================================================
    # PROCESS ONE ARTICLE
    # ============================================================

    def process_article(
        self,
        news,
        groups,
    ):

        logger.info(
            f"Processing article: "
            f"{news.title}"
        )

        # ========================================================
        # EXTRACT ARTICLE
        # ========================================================

        article_text = (
            ArticleExtractor.extract(
                news.url
            )
        )

        if not article_text:

            logger.warning(
                f"Could not extract article: "
                f"{news.url}"
            )

            return

        logger.info(
            f"Article extracted: "
            f"{len(article_text)} characters"
        )

        # ========================================================
        # SOURCE
        # ========================================================

        source_name = (
            news.source.name
            if getattr(news, "source", None)
            else "Unknown"
        )

        # ========================================================
        # AI GENERATION
        # ========================================================

        try:

            ai_response = (
                self.ai.generate(
                    title=news.title,
                    article=article_text,
                    source=source_name,
                )
            )

        except Exception as exc:

            logger.exception(
                f"AI generation failed for "
                f"{news.title}: {exc}"
            )

            return

        # ========================================================
        # VERIFY AI RESPONSE
        # ========================================================

        if not isinstance(
            ai_response,
            AIResponse,
        ):

            logger.error(
                "AI service did not return "
                "an AIResponse object."
            )

            return

        # ========================================================
        # FORMAT TELEGRAM MESSAGE
        # ========================================================

        message = (
            self.format_telegram_message(
                news,
                ai_response,
            )
        )

        # ========================================================
        # SEND TO ALL ENABLED CHATS
        # ========================================================

        success_count = 0

        for group in groups:

            try:

                self.telegram.send_message(
                    chat_id=group.chat_id,
                    message=message,
                )

                success_count += 1

                logger.info(
                    f"Article sent successfully to "
                    f"{group.title}"
                )

            except Exception as exc:

                logger.exception(
                    f"Failed to send article to "
                    f"{group.title}: {exc}"
                )

        # ========================================================
        # MARK POSTED
        # ========================================================

        if success_count == len(groups):

            self.news_repo.mark_posted(
                news.id
            )

            logger.info(
                f"Article marked posted: "
                f"{news.title}"
            )

        else:

            logger.warning(
                f"Article NOT marked posted. "
                f"{success_count}/{len(groups)} "
                f"chats succeeded."
            )

    # ============================================================
    # TELEGRAM FORMAT
    # ============================================================

    @staticmethod
    def format_telegram_message(
        news,
        ai: AIResponse,
    ):
        """
        Create a clean and professional Telegram news post.

        The message intentionally keeps the normal post compact.
        """

        # ========================================================
        # HEADLINE
        # ========================================================

        headline = (
            ai.headline
            or news.title
            or "Latest News"
        )

        # ========================================================
        # SUMMARY
        # ========================================================

        summary = (
            ai.summary
            or news.summary
            or ""
        )

        summary = str(summary).strip()

        # ========================================================
        # CATEGORY
        # ========================================================

        category = (
            ai.category
            or getattr(news, "category", None)
            or "News"
        )

        category = str(category).strip()

        category_lower = category.lower()

        # ========================================================
        # CATEGORY ICON
        # ========================================================

        category_icons = {

            "politics": "🏛️",
            "political": "🏛️",

            "india": "🇮🇳",

            "world": "🌍",
            "international": "🌍",

            "business": "💼",
            "economy": "📈",
            "finance": "💰",

            "technology": "💻",
            "technology & ai": "🤖",
            "tech": "💻",
            "ai": "🤖",
            "artificial intelligence": "🤖",

            "science": "🔬",

            "health": "🏥",

            "sports": "🏆",

            "entertainment": "🎬",

            "education": "🎓",

            "environment": "🌱",

            "security": "🛡️",
            "cybersecurity": "🔐",

            "crime": "🚨",

            "defence": "🪖",
            "defense": "🪖",

            "weather": "🌦️",

        }

        category_icon = "📰"

        for key, icon in category_icons.items():

            if key in category_lower:

                category_icon = icon

                break

        # ========================================================
        # MESSAGE START
        # ========================================================

        message = (
            f"📰 <b>{headline}</b>\n\n"
            f"{category_icon} "
            f"<b>{category.upper()}</b>\n\n"
        )

        # ========================================================
        # SUMMARY
        # ========================================================

        if summary:

            message += (
                f"{summary}\n\n"
            )

        # ========================================================
        # DIVIDER
        # ========================================================

        message += (
            "━━━━━━━━━━━━━━━━━━\n\n"
        )

        # ========================================================
        # KEY HIGHLIGHTS
        # ========================================================

        if ai.highlights:

            valid_highlights = [
                str(item).strip()
                for item in ai.highlights
                if item
            ]

            if valid_highlights:

                message += (
                    "🔎 <b>KEY HIGHLIGHTS</b>\n\n"
                )

                for item in valid_highlights[:5]:

                    message += (
                        f"• {item}\n"
                    )

                message += "\n"

        # ========================================================
        # AI EXPLAINS
        # ========================================================

        if ai.ai_explains:

            explanation = (
                str(ai.ai_explains).strip()
            )

            if explanation:

                message += (
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    "🧠 <b>AI EXPLAINS</b>\n\n"
                    f"{explanation}\n\n"
                )

        # ========================================================
        # WHY IT MATTERS / ANALYSIS
        # ========================================================

        if ai.sections:

            valid_sections = [
                str(item).strip()
                for item in ai.sections
                if item
            ]

            if valid_sections:

                message += (
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    "💡 <b>WHY IT MATTERS</b>\n\n"
                )

                for section in valid_sections[:2]:

                    message += (
                        f"• {section}\n"
                    )

                message += "\n"

        # ========================================================
        # IMPORTANT TERMS
        # ========================================================

        if ai.important_terms:

            terms = []

            for term in ai.important_terms[:6]:

                if not term:
                    continue

                clean_term = (
                    str(term)
                    .strip()
                    .replace("`", "")
                )

                if clean_term:

                    terms.append(
                        f"<code>{clean_term}</code>"
                    )

            if terms:

                message += (
                    "━━━━━━━━━━━━━━━━━━\n\n"
                    "🏷️ <b>IMPORTANT TERMS</b>\n\n"
                    + " ".join(terms)
                    + "\n\n"
                )

        # ========================================================
        # SOURCE
        # ========================================================

        if news.url:

            message += (
                "━━━━━━━━━━━━━━━━━━\n\n"
                f'🔗 <a href="{news.url}">'
                f"<b>Read Full Article</b>"
                f"</a>\n"
            )

        # ========================================================
        # HASHTAGS
        # ========================================================

        if ai.hashtags:

            hashtags = []

            for hashtag in ai.hashtags[:6]:

                if not hashtag:
                    continue

                clean_hashtag = (
                    str(hashtag)
                    .strip()
                    .replace(" ", "")
                )

                if not clean_hashtag.startswith("#"):

                    clean_hashtag = (
                        "#" + clean_hashtag
                    )

                hashtags.append(
                    clean_hashtag
                )

            if hashtags:

                message += (
                    "\n"
                    + " ".join(hashtags)
                    + "\n"
                )

        # ========================================================
        # FOOTER
        # ========================================================

        message += (
            "\n"
            "🤖 <b>AI News Agent</b>"
        )

        return message