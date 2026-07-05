"""Add moderation tables: reports and blocks.

Revision ID: 004
Revises: 003
Create Date: 2026-07-06

FR-MOD-001..003: users can report content, report users, and block users.
One open report per (reporter, target); one block per (blocker, blocked).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "reporter_user_id",
            sa.String(36),
            sa.ForeignKey("users.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("target_type", sa.String(16), nullable=False),
        sa.Column("target_id", sa.String(36), nullable=False, index=True),
        sa.Column("reason", sa.String(48), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("status", sa.String(16), server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("reporter_user_id", "target_type", "target_id"),
    )
    op.create_table(
        "blocks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "blocker_user_id",
            sa.String(36),
            sa.ForeignKey("users.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("blocked_user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("blocker_user_id", "blocked_user_id"),
    )


def downgrade() -> None:
    op.drop_table("blocks")
    op.drop_table("reports")
