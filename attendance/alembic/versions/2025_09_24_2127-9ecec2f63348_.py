"""empty message

Revision ID: 9ecec2f63348
Revises: 310dc112331c
Create Date: 2025-09-24 21:27:56.881285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ecec2f63348"
down_revision: Union[str, Sequence[str], None] = "310dc112331c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "departments",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_departments")),
        sa.UniqueConstraint("name", name=op.f("uq_departments_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("departments")
