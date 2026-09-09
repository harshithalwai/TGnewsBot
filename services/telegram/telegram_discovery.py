from loguru import logger

from repositories.telegram_group_repository import (
    TelegramGroupRepository,
)


class TelegramDiscoveryService:
    """
    Automatically discovers Telegram groups/channels
    when the bot is added or removed.

    Newly discovered chats are automatically enabled
    for news posting.
    """

    def __init__(self):

        self.group_repo = (
            TelegramGroupRepository()
        )

    # ========================================================
    # PROCESS MY CHAT MEMBER UPDATE
    # ========================================================

    async def process_my_chat_member(
        self,
        update,
    ):

        member_update = (
            update.my_chat_member
        )

        if not member_update:

            return False

        chat = member_update.chat

        if not chat:

            return False

        new_status = (
            member_update.new_chat_member.status
        )

        chat_id = chat.id

        chat_type = getattr(
            chat.type,
            "value",
            str(chat.type),
        )

        title = (
            self._get_chat_title(chat)
        )

        logger.info(
            f"Telegram chat update | "
            f"title={title} | "
            f"chat_id={chat_id} | "
            f"type={chat_type} | "
            f"status={new_status}"
        )

        # ====================================================
        # BOT ACTIVE
        # ====================================================

        if new_status in (
            "member",
            "administrator",
        ):

            self._activate_chat(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

            return True

        # ====================================================
        # BOT REMOVED
        # ====================================================

        if new_status in (
            "left",
            "kicked",
        ):

            self._deactivate_chat(
                chat_id=chat_id,
            )

            return False

        return False

    # ========================================================
    # GET CHAT TITLE
    # ========================================================

    @staticmethod
    def _get_chat_title(chat):

        title = getattr(
            chat,
            "title",
            None,
        )

        if title:

            return title

        username = getattr(
            chat,
            "username",
            None,
        )

        if username:

            return f"@{username}"

        first_name = getattr(
            chat,
            "first_name",
            None,
        )

        if first_name:

            return first_name

        return "Telegram Chat"

    # ========================================================
    # ACTIVATE CHAT
    # ========================================================

    def _activate_chat(
        self,
        chat_id: int,
        title: str,
        chat_type: str,
    ):

        existing = (
            self.group_repo.get_by_chat_id(
                chat_id
            )
        )

        # ====================================================
        # EXISTING CHAT
        # ====================================================

        if existing:

            self.group_repo.activate(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

            logger.info(
                f"Telegram chat activated: "
                f"{title} ({chat_id})"
            )

            return

        # ====================================================
        # NEW CHAT
        # ====================================================

        self.group_repo.create(
            chat_id=chat_id,
            title=title,
            chat_type=chat_type,
        )

        logger.info(
            f"NEW Telegram chat automatically "
            f"registered and enabled: "
            f"{title} ({chat_id})"
        )

    # ========================================================
    # DEACTIVATE CHAT
    # ========================================================

    def _deactivate_chat(
        self,
        chat_id: int,
    ):

        self.group_repo.deactivate(
            chat_id
        )

        logger.info(
            f"Telegram chat deactivated: "
            f"{chat_id}"
        )