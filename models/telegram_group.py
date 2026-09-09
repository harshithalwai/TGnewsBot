from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.sql import func

from database.base import Base


class TelegramGroup(Base):

    __tablename__ = "telegram_groups"

    # ============================================================
    # ID
    # ============================================================

    id = Column(
        Integer,
        primary_key=True,
    )

    # ============================================================
    # TELEGRAM CHAT ID
    # ============================================================

    chat_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    # ============================================================
    # CHAT TITLE
    # ============================================================

    title = Column(
        String(255),
        nullable=False,
    )

    # ============================================================
    # CHAT TYPE
    # ============================================================

    chat_type = Column(
        String(50),
        nullable=False,
    )

    # ============================================================
    # ACTIVE
    # ============================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # ============================================================
    # NEWS ENABLED
    # ============================================================

    news_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # ============================================================
    # CREATED AT
    # ============================================================

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )

    # ============================================================
    # UPDATED AT
    # ============================================================

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
    )