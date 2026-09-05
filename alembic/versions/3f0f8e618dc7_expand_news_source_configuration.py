"""expand news source configuration

Revision ID: 3f0f8e618dc7
Revises: a6b271688bfd
Create Date: 2026-09-04 22:30:48.984788

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f0f8e618dc7"
down_revision: Union[str, Sequence[str], None] = "a6b271688bfd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "sources",
        sa.Column(
            "source_type",
            sa.String(length=50),
            nullable=False,
            server_default="rss",
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "category",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "country",
            sa.String(length=100),
            nullable=True,
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "language",
            sa.String(length=50),
            nullable=True,
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "priority",
            sa.Integer(),
            nullable=False,
            server_default="5",
        ),
    )

    op.add_column(
        "sources",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    op.alter_column(
        "sources",
        "url",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=1000),
        existing_nullable=False,
    )

    # Remove migration-only defaults.
    op.alter_column(
        "sources",
        "source_type",
        server_default=None,
    )

    op.alter_column(
        "sources",
        "priority",
        server_default=None,
    )

    op.alter_column(
        "sources",
        "is_active",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "sources",
        "url",
        existing_type=sa.String(length=1000),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )

    op.drop_column("sources", "is_active")
    op.drop_column("sources", "priority")
    op.drop_column("sources", "language")
    op.drop_column("sources", "country")
    op.drop_column("sources", "category")
    op.drop_column("sources", "source_type")