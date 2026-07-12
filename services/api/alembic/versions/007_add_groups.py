"""Add groups and group_members tables.

Revision ID: 007
Revises: 006
Create Date: 2026-07-12

FR-SOC-006: wildlife communities with a shared roster, feed, and
leaderboard.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "groups",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("description", sa.String(280), nullable=True),
        sa.Column("cover_asset", sa.String(120), nullable=True),
        sa.Column("is_public", sa.Boolean(), server_default=sa.true()),
        sa.Column("created_by", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "group_members",
        sa.Column("group_id", sa.String(36), sa.ForeignKey("groups.id"), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("role", sa.String(16), server_default="member"),
        sa.Column("joined_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_group_members_user", "group_members", ["user_id", "group_id"])


def downgrade() -> None:
    op.drop_index("ix_group_members_user", table_name="group_members")
    op.drop_table("group_members")
    op.drop_table("groups")
