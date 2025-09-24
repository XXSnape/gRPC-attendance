"""empty message

Revision ID: 6335d8159560
Revises: b503ff89d87e
Create Date: 2025-09-24 21:58:14.585475

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6335d8159560"
down_revision: Union[str, Sequence[str], None] = "b503ff89d87e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "schedules",
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("lesson_id", sa.UUID(), nullable=False),
        sa.Column("audience_id", sa.UUID(), nullable=False),
        sa.Column("teacher_id", sa.UUID(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "number >= 1 AND number <= 6", name=op.f("ck_schedules_idx_number")
        ),
        sa.ForeignKeyConstraint(
            ["audience_id"],
            ["audiences.id"],
            name=op.f("fk_schedules_audience_id_audiences"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_schedules_group_id_groups"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
            name=op.f("fk_schedules_lesson_id_lessons"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["users.id"],
            name=op.f("fk_schedules_teacher_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedules")),
        sa.UniqueConstraint(
            "group_id",
            "lesson_id",
            "audience_id",
            "teacher_id",
            "number",
            "date",
            name="idx_uniq_group_lesson",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("schedules")
