from sqlalchemy import select

from database.session import SessionLocal
from models.telegram_group import TelegramGroup


class TelegramGroupRepository:

    # ============================================================
    # GET ACTIVE GROUPS
    # ============================================================

    def get_active(self):

        with SessionLocal() as session:

            stmt = (
                select(TelegramGroup)
                .where(
                    TelegramGroup.is_active == True
                )
                .order_by(
                    TelegramGroup.title
                )
            )

            return session.scalars(
                stmt
            ).all()


    # ============================================================
    # GET BY CHAT ID
    # ============================================================

    def get_by_chat_id(
        self,
        chat_id: int,
    ):

        with SessionLocal() as session:

            stmt = (
                select(TelegramGroup)
                .where(
                    TelegramGroup.chat_id == chat_id
                )
            )

            return session.scalar(stmt)


    # ============================================================
    # CREATE
    # ============================================================

    def create(
        self,
        chat_id: int,
        title: str,
        chat_type: str,
    ):

        with SessionLocal() as session:

            # Safety check against duplicate records.
            existing = session.scalar(
                select(TelegramGroup).where(
                    TelegramGroup.chat_id == chat_id
                )
            )

            if existing:

                return existing


            group = TelegramGroup(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
                is_active=True,
            )

            session.add(group)

            session.commit()

            session.refresh(group)

            return group


    # ============================================================
    # ACTIVATE
    # ============================================================

    def activate(
        self,
        chat_id: int,
    ):

        with SessionLocal() as session:

            group = session.scalar(
                select(TelegramGroup).where(
                    TelegramGroup.chat_id == chat_id
                )
            )

            if not group:

                return None


            group.is_active = True

            session.commit()

            session.refresh(group)

            return group


    # ============================================================
    # DEACTIVATE
    # ============================================================

    def deactivate(
        self,
        chat_id: int,
    ):

        with SessionLocal() as session:

            group = session.scalar(
                select(TelegramGroup).where(
                    TelegramGroup.chat_id == chat_id
                )
            )

            if not group:

                return None


            group.is_active = False

            session.commit()

            session.refresh(group)

            return group