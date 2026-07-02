"""Create initial Sprint 1 tables.

Revision ID: 001
Revises:
Create Date: 2026-07-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("status", sa.String(32), server_default="active"),
        sa.Column("age_band", sa.String(16), nullable=True),
        sa.Column("home_region", sa.String(8), nullable=True),
        sa.Column("trust_state", sa.String(32), server_default="neutral"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_status", "users", ["status"])

    op.create_table(
        "media_assets",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("owner_user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("file_name", sa.String(256)),
        sa.Column("content_type", sa.String(64)),
        sa.Column("byte_size", sa.BigInteger),
        sa.Column("sha256", sa.String(64)),
        sa.Column("storage_key", sa.String(512), nullable=True),
        sa.Column("asset_kind", sa.String(32), server_default="original"),
        sa.Column("processing_state", sa.String(32), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_media_assets_owner", "media_assets", ["owner_user_id"])
    op.create_index("ix_media_assets_processing", "media_assets", ["processing_state"])

    op.create_table(
        "media_derivatives",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("media_asset_id", sa.String(36), sa.ForeignKey("media_assets.id")),
        sa.Column("size_label", sa.String(32)),
        sa.Column("storage_key", sa.String(512)),
        sa.Column("exif_stripped", sa.Boolean, server_default="false"),
        sa.Column("visibility_state", sa.String(32), server_default="public"),
        sa.UniqueConstraint("media_asset_id", "size_label"),
    )

    op.create_table(
        "submissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("primary_media_asset_id", sa.String(36), sa.ForeignKey("media_assets.id")),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("visibility", sa.String(16), server_default="private"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_submissions_user", "submissions", ["user_id"])
    op.create_index("ix_submissions_status", "submissions", ["status"])

    op.create_table(
        "submission_attributes",
        sa.Column("submission_id", sa.String(36), sa.ForeignKey("submissions.id"), primary_key=True),
        sa.Column("animal_context", sa.String(16)),
        sa.Column("real_name", sa.String(256)),
        sa.Column("cute_name", sa.String(256)),
        sa.Column("caption", sa.Text),
        sa.Column("tags", sa.Text, nullable=True),
    )

    op.create_table(
        "capture_locations",
        sa.Column("submission_id", sa.String(36), sa.ForeignKey("submissions.id"), primary_key=True),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("accuracy_meters", sa.Float, nullable=True),
        sa.Column("source", sa.String(32), server_default="gps"),
        sa.Column("captured_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "public_location_cells",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("submission_id", sa.String(36), sa.ForeignKey("submissions.id")),
        sa.Column("cell_id", sa.String(32)),
        sa.Column("precision_label", sa.String(16), server_default="coarse"),
        sa.Column("available_after", sa.DateTime(timezone=True), nullable=True),
        sa.Column("suppressed_reason", sa.String(64), nullable=True),
    )
    op.create_index("ix_public_cells_cell", "public_location_cells", ["cell_id"])

    op.create_table(
        "score_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("submission_id", sa.String(36), sa.ForeignKey("submissions.id")),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("ledger", sa.String(32)),
        sa.Column("points", sa.Integer, nullable=True),
        sa.Column("event_type", sa.String(32)),
        sa.Column("formula_version", sa.String(32), nullable=True),
        sa.Column("explanation_category", sa.String(32), nullable=True),
        sa.Column("previous_state", sa.String(32), nullable=True),
        sa.Column("new_state", sa.String(32)),
        sa.Column("actor", sa.String(64), server_default="system"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_score_events_user", "score_events", ["user_id"])
    op.create_index("ix_score_events_submission", "score_events", ["submission_id"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor_user_id", sa.String(36), nullable=True),
        sa.Column("action", sa.String(64)),
        sa.Column("target_type", sa.String(32)),
        sa.Column("target_id", sa.String(36), nullable=True),
        sa.Column("metadata_json", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_logs_actor", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_target", "audit_logs", ["target_type", "target_id"])

    op.create_table(
        "idempotency_keys",
        sa.Column("key", sa.String(128), primary_key=True),
        sa.Column("user_id", sa.String(36)),
        sa.Column("operation", sa.String(64)),
        sa.Column("request_hash", sa.String(64), nullable=True),
        sa.Column("response_ref", sa.String(256), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("idempotency_keys")
    op.drop_table("audit_logs")
    op.drop_table("score_events")
    op.drop_table("public_location_cells")
    op.drop_table("capture_locations")
    op.drop_table("submission_attributes")
    op.drop_table("submissions")
    op.drop_table("media_derivatives")
    op.drop_table("media_assets")
    op.drop_table("users")
