"""Add social tables: reactions, comments, stories, story_views.

Revision ID: 005
Revises: 004
Create Date: 2026-07-10

FR-SOC-001..004: persisted multi-kind reactions, flat comments with
soft delete, 24-hour stories, and story view tracking.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reactions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "submission_id",
            sa.String(36),
            sa.ForeignKey("submissions.id"),
            nullable=False,
            index=True,
        ),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "submission_id"),
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "submission_id", sa.String(36), sa.ForeignKey("submissions.id"), nullable=False
        ),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("body", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_comments_submission_created", "comments", ["submission_id", "created_at"]
    )
    op.create_table(
        "stories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "media_asset_id", sa.String(36), sa.ForeignKey("media_assets.id"), nullable=False
        ),
        sa.Column("caption", sa.String(280), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False, index=True),
    )
    op.create_index("ix_stories_user_expires", "stories", ["user_id", "expires_at"])
    op.create_table(
        "story_views",
        sa.Column("story_id", sa.String(36), sa.ForeignKey("stories.id"), primary_key=True),
        sa.Column("viewer_id", sa.String(36), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("viewed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("story_views")
    op.drop_table("stories")
    op.drop_table("comments")
    op.drop_table("reactions")
