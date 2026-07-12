from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    news: Mapped[list["News"]] = relationship(
        "News",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Source(name='{self.name}')>"