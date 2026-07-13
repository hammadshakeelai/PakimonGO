"""Add group_quests table.

Revision ID: 008
Revises: 007
Create Date: 2026-07-13

FR-SOC-007: time-boxed community challenges whose progress is computed
live from members' scored captures inside the quest window.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "group_quests",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("group_id", sa.String(36), sa.ForeignKey("groups.id"), nullable=False),
        sa.Column("title", sa.String(120), nullable=False),
        sa.Column("description", sa.String(280), nullable=True),
        sa.Column("kind", sa.String(16), server_default="captures"),
        sa.Column("target", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_group_quests_group_id", "group_quests", ["group_id"])
    op.create_index("ix_group_quests_ends_at", "group_quests", ["ends_at"])


def downgrade() -> None:
    op.drop_index("ix_group_quests_ends_at", table_name="group_quests")
    op.drop_index("ix_group_quests_group_id", table_name="group_quests")
    op.drop_table("group_quests")
