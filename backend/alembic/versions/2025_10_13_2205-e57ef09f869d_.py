"""empty message

Revision ID: e57ef09f869d
Revises: 4b36a1b62395
Create Date: 2025-10-13 22:05:04.959332

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e57ef09f869d"
down_revision: Union[str, Sequence[str], None] = "4b36a1b62395"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "group_numbers",
        sa.Column("year_of_admission", sa.Integer(), nullable=False),
    )
    op.drop_constraint(
        op.f("idx_uniq_number_group"),
        "group_numbers",
        type_="unique",
    )
    op.create_unique_constraint(
        "idx_uniq_number_group",
        "group_numbers",
        ["group_id", "number", "year_of_admission"],
    )
    op.drop_constraint(
        op.f("idx_uniq_user_group"),
        "students_groups",
        type_="unique",
    )
    op.create_unique_constraint(
        "idx_uniq_user_group",
        "students_groups",
        ["student_id", "group_id"],
    )
    op.drop_column("students_groups", "year_of_admission")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "students_groups",
        sa.Column(
            "year_of_admission",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        "idx_uniq_user_group", "students_groups", type_="unique"
    )
    op.create_unique_constraint(
        op.f("idx_uniq_user_group"),
        "students_groups",
        ["student_id", "group_id", "year_of_admission"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_constraint(
        "idx_uniq_number_group", "group_numbers", type_="unique"
    )
    op.create_unique_constraint(
        op.f("idx_uniq_number_group"),
        "group_numbers",
        ["group_id", "number"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("group_numbers", "year_of_admission")
