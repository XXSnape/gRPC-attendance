"""empty message

Revision ID: 6701385d7eda
Revises: 8f67cb320fc2
Create Date: 2025-10-11 21:08:28.331248

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6701385d7eda"
down_revision: Union[str, Sequence[str], None] = "8f67cb320fc2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("uq_users_email"), "users", type_="unique"
    )
    op.create_index(
        op.f("ix_users_email"), "users", ["email"], unique=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_unique_constraint(
        op.f("uq_users_email"),
        "users",
        ["email"],
        postgresql_nulls_not_distinct=False,
    )
