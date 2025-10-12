"""empty message

Revision ID: 1933a66cd3fe
Revises: 6701385d7eda
Create Date: 2025-10-12 15:07:22.980465

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1933a66cd3fe"
down_revision: Union[str, Sequence[str], None] = "6701385d7eda"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    type_of_lesson_enum = sa.Enum(
        "LECTURE",
        "PRACTICAL",
        "LAB",
        "EXAM",
        "TEST",
        name="typeoflessonenum",
    )
    type_of_lesson_enum.create(op.get_bind())

    op.add_column(
        "schedules",
        sa.Column(
            "abc",
            type_of_lesson_enum,
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("schedules", "abc")
    type_of_lesson_enum = sa.Enum(
        "LECTURE",
        "PRACTICAL",
        "LAB",
        "EXAM",
        "TEST",
        name="typeoflessonenum",
    )
    type_of_lesson_enum.drop(op.get_bind())
