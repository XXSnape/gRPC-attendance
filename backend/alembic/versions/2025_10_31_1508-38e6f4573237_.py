"""empty message

Revision ID: 38e6f4573237
Revises: e3a82eabee93
Create Date: 2025-10-31 15:08:09.665229

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "38e6f4573237"
down_revision: Union[str, Sequence[str], None] = "e3a82eabee93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "type",
        new_column_name="role",
        existing_type=sa.String(),
        nullable=False,
    )
    op.create_unique_constraint(
        "idx_uniq_lesson_department",
        "lessons",
        ["name", "department_id"],
    )
    op.drop_column("lessons", "on_schedule")
    op.add_column(
        "schedules",
        sa.Column(
            "is_standardized",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "type", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "role")
    op.drop_column("schedules", "is_standardized")
    op.add_column(
        "lessons",
        sa.Column(
            "on_schedule",
            sa.BOOLEAN(),
            server_default=sa.text("true"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        "idx_uniq_lesson_department", "lessons", type_="unique"
    )
