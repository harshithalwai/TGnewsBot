from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes,
)

from config.settings import BOT_TOKEN

from repositories.telegram_group_repository import (
    TelegramGroupRepository,
)

from services.telegram.telegram_discovery import (
    TelegramDiscoveryService,
)


class TelegramBot:

    def __init__(
        self,
        scheduler_service,
    ):

        self.scheduler_service = (
            scheduler_service
        )

        self.group_repo = (
            TelegramGroupRepository()
        )

        self.discovery_service = (
            TelegramDiscoveryService()
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

        # ========================================================
        # CHAT DISCOVERY
        # ========================================================

        self.application.add_handler(
            ChatMemberHandler(
                self.chat_member_update,
                ChatMemberHandler.MY_CHAT_MEMBER,
            )
        )

    # ============================================================
    # CHAT MEMBER UPDATE
    # ============================================================

    async def chat_member_update(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        try:

            chat_active = (
                await self.discovery_service
                .process_my_chat_member(
                    update
                )
            )

            # Scheduler is already started by main.py.
            #
            # We do NOT need to start it here.
            #
            # The discovery service only registers
            # the Telegram chat.

            if chat_active:

                print(
                    "Telegram chat automatically "
                    "enabled for news."
                )

        except Exception as exc:

            print(
                f"Telegram discovery error: {exc}"
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

        chat_type = getattr(
            chat.type,
            "value",
            str(chat.type),
        )

        existing = (
            self.group_repo.get_by_chat_id(
                chat_id
            )
        )

        if existing:

            self.group_repo.enable_news(
                chat_id
            )

            self.group_repo.activate(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

        else:

            self.group_repo.create(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

        if update.message:

            await update.message.reply_text(

                "✅ <b>AI News Bot</b>\n\n"

                f"📢 <b>Chat:</b> {title}\n\n"

                "📰 News posting is now ACTIVE "
                "for this chat.\n\n"

                "⏱ Automatic news processing is "
                "already running.",

                parse_mode="HTML",
            )

    # ============================================================
    # /END
    # ============================================================

    async def end_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        chat = update.effective_chat

        if not chat:

            return

        chat_id = chat.id

        self.group_repo.disable_news(
            chat_id
        )

        if update.message:

            await update.message.reply_text(

                "🛑 <b>News Disabled</b>\n\n"

                "Automatic news posting has been "
                "disabled for this chat.\n\n"

                "Other enabled chats will continue "
                "receiving news.\n\n"

                "Use /start to enable it again.",

                parse_mode="HTML",
            )

    # ============================================================
    # /STATUS
    # ============================================================

    async def status_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ):

        chat = update.effective_chat

        if not chat:

            return

        chat_id = chat.id

        group = (
            self.group_repo.get_by_chat_id(
                chat_id
            )
        )

        scheduler_running = (
            self.scheduler_service.get_status()
        )

        if not group:

            chat_status = "NOT REGISTERED"

        elif not group.is_active:

            chat_status = "INACTIVE"

        elif not group.news_enabled:

            chat_status = "NEWS DISABLED"

        else:

            chat_status = "🟢 ACTIVE"

        scheduler_status = (
            "🟢 RUNNING"
            if scheduler_running
            else "🔴 STOPPED"
        )

        if update.message:

            await update.message.reply_text(

                "📊 <b>AI News Bot Status</b>\n\n"

                f"Chat: <b>{chat_status}</b>\n\n"

                f"Scheduler: "
                f"<b>{scheduler_status}</b>\n\n"

                "⏱ Interval: 1 minute\n\n"

                "Commands:\n"
                "/start - Enable news\n"
                "/end - Disable news\n"
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

        if update.message:

            await update.message.reply_text(

                "🤖 <b>AI News Bot</b>\n\n"

                "News starts automatically when "
                "the bot is running.\n\n"

                "/start\n"
                "Enable news for this chat.\n\n"

                "/end\n"
                "Disable news for this chat.\n\n"

                "/status\n"
                "Check this chat's status.\n\n"

                "/help\n"
                "Show this help.",

                parse_mode="HTML",
            )

    # ============================================================
    # RUN
    # ============================================================

    def run(self):

        print()
        print("=" * 60)
        print("TELEGRAM BOT STARTED")
        print("=" * 60)

        print(
            "Commands: "
            "/start /end /status /help"
        )

        print(
            "Automatic chat discovery: ENABLED"
        )

        print(
            "News scheduler: ALREADY RUNNING"
        )

        print("=" * 60)

        self.application.run_polling(
            drop_pending_updates=False
        )