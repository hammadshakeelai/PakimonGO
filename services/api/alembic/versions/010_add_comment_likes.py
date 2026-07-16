"""Add comment_likes table.

Revision ID: 010
Revises: 009
Create Date: 2026-07-17

FR-SOC-009: hearts on comments (one per user per comment, toggled).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comment_likes",
        sa.Column("comment_id", sa.String(36), sa.ForeignKey("comments.id"), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("comment_likes")
