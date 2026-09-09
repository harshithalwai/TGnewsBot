from database.session import SessionLocal

from models.telegram_group import TelegramGroup


class TelegramGroupRepository:

    def __init__(self):
        pass

    # ============================================================
    # GET BY CHAT ID
    # ============================================================

    def get_by_chat_id(
        self,
        chat_id,
    ):

        db = SessionLocal()

        try:

            return (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.chat_id == chat_id
                )
                .first()
            )

        finally:

            db.close()

    # ============================================================
    # CREATE
    # ============================================================

    def create(
        self,
        chat_id,
        title,
        chat_type,
    ):

        db = SessionLocal()

        try:

            group = TelegramGroup(

                chat_id=chat_id,

                title=title,

                chat_type=chat_type,

                is_active=True,

                # IMPORTANT:
                # Newly discovered chats are enabled automatically.
                news_enabled=True,
            )

            db.add(group)

            db.commit()

            db.refresh(group)

            return group

        finally:

            db.close()

    # ============================================================
    # ACTIVATE
    # ============================================================

    def activate(
        self,
        chat_id,
        title,
        chat_type,
    ):

        db = SessionLocal()

        try:

            group = (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.chat_id == chat_id
                )
                .first()
            )

            # ----------------------------------------------------
            # CHAT DOES NOT EXIST
            # ----------------------------------------------------

            if not group:

                return self._create_in_session(
                    db=db,
                    chat_id=chat_id,
                    title=title,
                    chat_type=chat_type,
                )

            # ----------------------------------------------------
            # CHAT EXISTS
            # ----------------------------------------------------

            group.is_active = True

            # IMPORTANT:
            # Re-activated chats automatically receive news.
            group.news_enabled = True

            group.title = title

            group.chat_type = chat_type

            db.commit()

            db.refresh(group)

            return group

        finally:

            db.close()

    # ============================================================
    # CREATE INSIDE EXISTING SESSION
    # ============================================================

    @staticmethod
    def _create_in_session(
        db,
        chat_id,
        title,
        chat_type,
    ):

        group = TelegramGroup(

            chat_id=chat_id,

            title=title,

            chat_type=chat_type,

            is_active=True,

            news_enabled=True,
        )

        db.add(group)

        db.commit()

        db.refresh(group)

        return group

    # ============================================================
    # DEACTIVATE
    # ============================================================

    def deactivate(
        self,
        chat_id,
    ):

        db = SessionLocal()

        try:

            group = (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.chat_id == chat_id
                )
                .first()
            )

            if not group:

                return False

            group.is_active = False

            group.news_enabled = False

            db.commit()

            return True

        finally:

            db.close()

    # ============================================================
    # ENABLE NEWS
    # ============================================================

    def enable_news(
        self,
        chat_id,
    ):

        db = SessionLocal()

        try:

            group = (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.chat_id == chat_id
                )
                .first()
            )

            if not group:

                return False

            group.news_enabled = True

            group.is_active = True

            db.commit()

            return True

        finally:

            db.close()

    # ============================================================
    # DISABLE NEWS
    # ============================================================

    def disable_news(
        self,
        chat_id,
    ):

        db = SessionLocal()

        try:

            group = (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.chat_id == chat_id
                )
                .first()
            )

            if not group:

                return False

            group.news_enabled = False

            db.commit()

            return True

        finally:

            db.close()

    # ============================================================
    # ACTIVE + NEWS ENABLED CHATS
    # ============================================================

    def get_news_enabled_groups(self):

        db = SessionLocal()

        try:

            return (
                db.query(TelegramGroup)
                .filter(
                    TelegramGroup.is_active.is_(True),
                    TelegramGroup.news_enabled.is_(True),
                )
                .all()
            )

        finally:

            db.close()