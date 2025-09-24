"""empty message

Revision ID: f3e3aed178c4
Revises: ede5bd5a68be
Create Date: 2025-09-24 21:24:12.208429

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3e3aed178c4"
down_revision: Union[str, Sequence[str], None] = "ede5bd5a68be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
