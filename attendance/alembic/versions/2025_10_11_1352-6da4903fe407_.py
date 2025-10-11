"""empty message

Revision ID: 6da4903fe407
Revises: 6dd94445089a
Create Date: 2025-10-11 13:52:15.721321

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6da4903fe407"
down_revision: Union[str, Sequence[str], None] = "6dd94445089a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users_groups",
        sa.Column(
            "is_prefect",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users_groups", "is_prefect")
