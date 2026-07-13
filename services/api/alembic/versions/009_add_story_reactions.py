"""Add story_reactions table.

Revision ID: 009
Revises: 008
Create Date: 2026-07-13

FR-SOC-008: quick emoji reactions to 24h stories (one per viewer per
story; re-reacting replaces the emoji).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "story_reactions",
        sa.Column("story_id", sa.String(36), sa.ForeignKey("stories.id"), primary_key=True),
        sa.Column("viewer_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("emoji", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("story_reactions")
