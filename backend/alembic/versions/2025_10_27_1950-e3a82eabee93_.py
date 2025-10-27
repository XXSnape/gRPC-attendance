"""empty message

Revision ID: e3a82eabee93
Revises: 61e02cf787b7
Create Date: 2025-10-27 19:50:49.839574

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e3a82eabee93"
down_revision: Union[str, Sequence[str], None] = "61e02cf787b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audiences_schedules",
        sa.Column("audience_id", sa.UUID(), nullable=False),
        sa.Column("schedule_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["audience_id"],
            ["audiences.id"],
            name=op.f(
                "fk_audiences_schedules_audience_id_audiences"
            ),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
            name=op.f(
                "fk_audiences_schedules_schedule_id_schedules"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_audiences_schedules")
        ),
        sa.UniqueConstraint(
            "audience_id",
            "schedule_id",
            name="idx_uniq_audience_schedule",
        ),
    )
    op.drop_constraint(
        op.f("idx_uniq_subgroup_schedule"),
        "groups_schedules",
        type_="unique",
    )
    op.create_unique_constraint(
        "idx_uniq_subgroup_schedule",
        "groups_schedules",
        ["group_id", "schedule_id"],
    )
    op.drop_column("groups_schedules", "subgroup_number")
    op.add_column(
        "schedules",
        sa.Column(
            "subgroup_number",
            sa.Integer(),
            server_default=sa.text("NULL"),
            nullable=True,
        ),
    )
    op.drop_constraint(
        op.f("idx_uniq_schedule"), "schedules", type_="unique"
    )
    op.create_unique_constraint(
        "idx_uniq_schedule",
        "schedules",
        [
            "type_of_lesson",
            "date",
            "number",
            "lesson_id",
            "subgroup_number",
        ],
    )
    op.drop_constraint(
        op.f("fk_schedules_audience_id_audiences"),
        "schedules",
        type_="foreignkey",
    )
    op.drop_column("schedules", "audience_id")
    op.drop_constraint(
        op.f("uq_specializations_code"),
        "specializations",
        type_="unique",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        op.f("uq_specializations_code"),
        "specializations",
        ["code"],
        postgresql_nulls_not_distinct=False,
    )
    op.add_column(
        "schedules",
        sa.Column(
            "audience_id",
            sa.UUID(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_foreign_key(
        op.f("fk_schedules_audience_id_audiences"),
        "schedules",
        "audiences",
        ["audience_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "idx_uniq_schedule", "schedules", type_="unique"
    )
    op.create_unique_constraint(
        op.f("idx_uniq_schedule"),
        "schedules",
        [
            "type_of_lesson",
            "date",
            "number",
            "lesson_id",
            "audience_id",
        ],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("schedules", "subgroup_number")
    op.add_column(
        "groups_schedules",
        sa.Column(
            "subgroup_number",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_constraint(
        "idx_uniq_subgroup_schedule",
        "groups_schedules",
        type_="unique",
    )
    op.create_unique_constraint(
        op.f("idx_uniq_subgroup_schedule"),
        "groups_schedules",
        ["subgroup_number", "group_id", "schedule_id"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_table("audiences_schedules")
