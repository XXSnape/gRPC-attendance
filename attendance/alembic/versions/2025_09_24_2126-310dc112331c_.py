"""empty message

Revision ID: 310dc112331c
Revises: f3e3aed178c4
Create Date: 2025-09-24 21:26:26.687948

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "310dc112331c"
down_revision: Union[str, Sequence[str], None] = "f3e3aed178c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "audiences",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "address",
            sa.Enum("PANTELEEVSKAYA", "ORDYNKA", "POTAPOVSKY", name="addressenum"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audiences")),
        sa.UniqueConstraint("name", "address", name="idx_uniq_name_address"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("audiences")
