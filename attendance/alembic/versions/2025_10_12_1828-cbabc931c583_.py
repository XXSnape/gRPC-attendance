"""empty message

Revision ID: cbabc931c583
Revises: 8e0eb92ba6ce
Create Date: 2025-10-12 18:28:19.550968

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "cbabc931c583"
down_revision: Union[str, Sequence[str], None] = "8e0eb92ba6ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "students_groups",
        sa.Column("number", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("students_groups", "number")
