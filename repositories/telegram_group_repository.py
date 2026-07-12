from sqlalchemy import select

from database.session import SessionLocal
from models.telegram_group import TelegramGroup


class TelegramGroupRepository:

    def get_active(self):

        with SessionLocal() as session:

            stmt = (
                select(TelegramGroup)
                .where(TelegramGroup.is_active == True)
            )

            return session.scalars(stmt).all()

    def get_by_chat_id(self, chat_id: int):

        with SessionLocal() as session:

            stmt = select(TelegramGroup).where(
                TelegramGroup.chat_id == chat_id
            )

            return session.scalar(stmt)

    def create(self, chat_id: int, title: str, chat_type: str):

        with SessionLocal() as session:

            group = TelegramGroup(
                chat_id=chat_id,
                title=title,
                chat_type=chat_type,
            )

            session.add(group)
            session.commit()
            session.refresh(group)

            return group