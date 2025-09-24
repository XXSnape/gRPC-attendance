"""empty message

Revision ID: e34f0ce0dac8
Revises: 6335d8159560
Create Date: 2025-09-24 21:58:52.527679

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e34f0ce0dac8"
down_revision: Union[str, Sequence[str], None] = "6335d8159560"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "teachers_departments",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("department_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
            name=op.f("fk_teachers_departments_department_id_departments"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_teachers_departments_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teachers_departments")),
        sa.UniqueConstraint(
            "user_id", "department_id", name="idx_uniq_teacher_department"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("teachers_departments")
