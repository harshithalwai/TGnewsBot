from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.base import Base


if TYPE_CHECKING:
    from models.source import Source


class News(Base):

    __tablename__ = "news"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
        nullable=False,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    ai_image: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )

    title_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )

    is_posted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )

    source: Mapped["Source"] = relationship(
        "Source",
        back_populates="news",
    )