"""Add sensitive_species table.

Revision ID: 003
Revises: 002
Create Date: 2026-07-05

The sensitive_species model existed but was never captured in a migration, so
the Postgres schema was missing it (dev used create_all on SQLite). Adds it so
the migration path matches the models.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sensitive_species",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("scientific_name", sa.String(256), nullable=False, unique=True),
        sa.Column("common_name", sa.String(256), nullable=True),
        sa.Column("suppression_level", sa.String(16), server_default="coarse_cell"),
        sa.Column("reason", sa.String(256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("sensitive_species")
