"""Add follows table for the social graph.

Revision ID: 006
Revises: 005
Create Date: 2026-07-11

FR-SOC-005: users can follow each other. One row per direction; the
reverse index serves "who follows me" lookups.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "follows",
        sa.Column("follower_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("followee_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_follows_followee", "follows", ["followee_id", "follower_id"])


def downgrade() -> None:
    op.drop_index("ix_follows_followee", table_name="follows")
    op.drop_table("follows")
