"""add news enabled to telegram groups

Revision ID: 00d963de645f
Revises: 81e3f5f896e8
Create Date: 2026-09-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "00d963de645f"
down_revision: Union[str, Sequence[str], None] = "81e3f5f896e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Add the column with a temporary server-side default.
    #
    # Existing Telegram groups/channels will receive TRUE.
    # This is important because the table already contains rows.
    op.add_column(
        "telegram_groups",
        sa.Column(
            "news_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

    # The default is only needed while adding/backfilling the column.
    # New records will use the SQLAlchemy model default.
    op.alter_column(
        "telegram_groups",
        "news_enabled",
        server_default=None,
    )

    # These were also detected by Alembic because your model contains
    # updated_at and an index on chat_id.
    #
    # Only keep these if they are genuinely missing from your database.

    op.add_column(
        "telegram_groups",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.alter_column(
        "telegram_groups",
        "updated_at",
        server_default=None,
    )

    op.drop_constraint(
        "telegram_groups_chat_id_key",
        "telegram_groups",
        type_="unique",
    )

    op.create_index(
        "ix_telegram_groups_chat_id",
        "telegram_groups",
        ["chat_id"],
        unique=True,
    )

def downgrade() -> None:

    op.drop_index(
        "ix_telegram_groups_chat_id",
        table_name="telegram_groups",
    )

    op.create_unique_constraint(
        "telegram_groups_chat_id_key",
        "telegram_groups",
        ["chat_id"],
    )

    op.drop_column(
        "telegram_groups",
        "updated_at",
    )

    op.drop_column(
        "telegram_groups",
        "news_enabled",
    )