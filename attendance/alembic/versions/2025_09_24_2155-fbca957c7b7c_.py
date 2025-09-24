"""empty message

Revision ID: fbca957c7b7c
Revises: d9c5317b5568
Create Date: 2025-09-24 21:55:42.807395

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fbca957c7b7c"
down_revision: Union[str, Sequence[str], None] = "d9c5317b5568"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "roles",
        sa.Column(
            "role",
            sa.Enum("STUDENT", "TEACHER", "ADMIN", name="roleenum"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roles")),
        sa.UniqueConstraint("role", name=op.f("uq_roles_role")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("roles")
