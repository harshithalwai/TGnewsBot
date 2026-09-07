from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config.settings import BOT_TOKEN

from repositories.telegram_group_repository import (
    TelegramGroupRepository,
)


class TelegramBot:

    def __init__(self, scheduler_service):

        self.scheduler_service = scheduler_service

        self.group_repo = (
            TelegramGroupRepository()
        )

        self.application = (
            Application.builder()
            .token(BOT_TOKEN)
            .build()
        )

        # ========================================================
        # COMMANDS
        # ========================================================

        self.application.add_handler(
            CommandHandler(
                "start",
                self.start_command,
            )
        )

        self.application.add_handler(
            CommandHandler(
                "end",
                self.end_command,
            )
        )

        self.application.add_handler(
            CommandHandler(
                "status",
                self.status_command,
            )
        )

        self.application.add_handler(
            CommandHandler(
                "help",
                self.help_command,
            )
        )


    # ============================================================
    # /START
    # ============================================================

    async def start_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        chat = update.effective_chat

        if not chat:
            return


        chat_id = chat.id

        title = (
            chat.title
            or chat.full_name
            or "Telegram Chat"
        )

        chat_type = chat.type


        print()
        print("=" * 60)
        print("TELEGRAM CHAT DETECTED")
        print("=" * 60)

        print(f"Chat ID   : {chat_id}")
        print(f"Title     : {title}")
        print(f"Chat type : {chat_type}")


        # ========================================================
        # REGISTER / ACTIVATE CHAT
        # ========================================================

        existing = (
            self.group_repo.get_by_chat_id(
                chat_id
            )
        )


        if existing:

            self.group_repo.activate(
                chat_id
            )

        else:

            self.group_repo.create(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )


        # ========================================================
        # START NEWS SYSTEM
        # ========================================================

        self.scheduler_service.start_news()


        await update.message.reply_text(

            "✅ <b>AI News Bot Started</b>\n\n"

            f"📢 <b>Chat:</b> {title}\n\n"

            "📰 News posting is now ACTIVE.\n"
            "⏱ New articles will be processed "
            "automatically every minute.\n\n"

            "Use /end to stop news posting.",

            parse_mode="HTML",
        )


        print(
            "Chat registered and news system started."
        )


    # ============================================================
    # /END
    # ============================================================

    async def end_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        self.scheduler_service.stop_news()


        await update.message.reply_text(

            "🛑 <b>AI News Bot Stopped</b>\n\n"

            "Automatic news posting has been stopped.\n\n"

            "Send /start to start it again.",

            parse_mode="HTML",
        )


        print(
            "News system stopped by Telegram command."
        )


    # ============================================================
    # /STATUS
    # ============================================================

    async def status_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        running = (
            self.scheduler_service.get_status()
        )


        if running:

            status = "🟢 RUNNING"

        else:

            status = "🔴 STOPPED"


        await update.message.reply_text(

            "📊 <b>AI News Bot Status</b>\n\n"

            f"Scheduler: <b>{status}</b>\n\n"

            "⏱ Interval: 1 minute\n\n"

            "Commands:\n"
            "/start - Start news posting\n"
            "/end - Stop news posting\n"
            "/status - Check status\n"
            "/help - Show help",

            parse_mode="HTML",
        )


    # ============================================================
    # /HELP
    # ============================================================

    async def help_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        await update.message.reply_text(

            "🤖 <b>AI News Bot</b>\n\n"

            "/start\n"
            "Start automatic news posting.\n\n"

            "/end\n"
            "Stop automatic news posting.\n\n"

            "/status\n"
            "Check scheduler status.\n\n"

            "/help\n"
            "Show this help.",

            parse_mode="HTML",
        )


    # ============================================================
    # RUN BOT
    # ============================================================

    def run(self):

        print()
        print("=" * 60)
        print("TELEGRAM BOT STARTED")
        print("=" * 60)

        print(
            "Commands: /start /end /status /help"
        )

        print("=" * 60)


        self.application.run_polling(
            drop_pending_updates=True
        )