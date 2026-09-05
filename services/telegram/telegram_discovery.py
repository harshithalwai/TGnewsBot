import threading
import time

import requests
from loguru import logger

from config.settings import BOT_TOKEN
from repositories.telegram_group_repository import (
    TelegramGroupRepository,
)


class TelegramDiscoveryService:

    BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

    POLL_TIMEOUT = 30

    def __init__(self):

        self.group_repo = TelegramGroupRepository()

        self.running = False

        self.thread = None

        self.offset = None

    # ============================================================
    # START
    # ============================================================

    def start(self):

        if not BOT_TOKEN:

            raise RuntimeError(
                "BOT_TOKEN is not configured."
            )

        if self.running:

            logger.warning(
                "Telegram discovery is already running."
            )

            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            name="TelegramDiscovery",
            daemon=True,
        )

        self.thread.start()

        logger.info(
            "Telegram automatic group/channel discovery started."
        )

    # ============================================================
    # STOP
    # ============================================================

    def stop(self):

        self.running = False

        logger.info(
            "Telegram discovery stopped."
        )

    # ============================================================
    # MAIN LOOP
    # ============================================================

    def _run(self):

        logger.info(
            "Listening for Telegram chat updates..."
        )

        while self.running:

            try:

                updates = self._get_updates()

                for update in updates:

                    self._process_update(update)

            except Exception as exc:

                logger.exception(
                    f"Telegram discovery error: {exc}"
                )

                time.sleep(5)

    # ============================================================
    # GET UPDATES
    # ============================================================

    def _get_updates(self):

        params = {
            "timeout": self.POLL_TIMEOUT,
            "allowed_updates": [
                "my_chat_member",
            ],
        }

        if self.offset is not None:

            params["offset"] = self.offset

        response = requests.get(
            f"{self.BASE_URL}/getUpdates",
            params=params,
            timeout=self.POLL_TIMEOUT + 10,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("ok"):

            raise RuntimeError(
                f"Telegram getUpdates failed: {data}"
            )

        updates = data.get(
            "result",
            [],
        )

        if updates:

            self.offset = (
                updates[-1]["update_id"] + 1
            )

        return updates

    # ============================================================
    # PROCESS UPDATE
    # ============================================================

    def _process_update(self, update):

        member_update = update.get(
            "my_chat_member"
        )

        if not member_update:

            return

        chat = member_update.get(
            "chat"
        )

        new_chat_member = member_update.get(
            "new_chat_member"
        )

        if not chat or not new_chat_member:

            return

        chat_id = chat.get(
            "id"
        )

        chat_type = chat.get(
            "type",
            "unknown",
        )

        title = self._get_chat_title(
            chat
        )

        new_status = new_chat_member.get(
            "status"
        )

        logger.info(
            f"Telegram chat update: "
            f"{title} | "
            f"{chat_id} | "
            f"type={chat_type} | "
            f"status={new_status}"
        )

        # ========================================================
        # BOT ADDED / ACTIVE
        # ========================================================

        if new_status in (
            "member",
            "administrator",
        ):

            self._activate_chat(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

        # ========================================================
        # BOT REMOVED
        # ========================================================

        elif new_status in (
            "left",
            "kicked",
        ):

            self._deactivate_chat(
                chat_id
            )

    # ============================================================
    # CHAT TITLE
    # ============================================================

    @staticmethod
    def _get_chat_title(chat):

        title = chat.get(
            "title"
        )

        if title:

            return title

        username = chat.get(
            "username"
        )

        if username:

            return f"@{username}"

        first_name = chat.get(
            "first_name"
        )

        if first_name:

            return first_name

        return "Telegram Chat"

    # ============================================================
    # ACTIVATE CHAT
    # ============================================================

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

        if existing:

            # Update metadata in case the
            # Telegram group/channel name changed.

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

        self.group_repo.create(
            chat_id=chat_id,
            title=title,
            chat_type=chat_type,
        )

        logger.info(
            f"NEW Telegram chat automatically registered: "
            f"{title} ({chat_id})"
        )

    # ============================================================
    # DEACTIVATE CHAT
    # ============================================================

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