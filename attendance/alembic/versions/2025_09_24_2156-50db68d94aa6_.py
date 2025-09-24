"""empty message

Revision ID: 50db68d94aa6
Revises: fbca957c7b7c
Create Date: 2025-09-24 21:56:36.876743

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50db68d94aa6"
down_revision: Union[str, Sequence[str], None] = "fbca957c7b7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users_roles",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk_users_roles_role_id_roles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_users_roles_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users_roles")),
        sa.UniqueConstraint("user_id", "role_id", name="idx_uniq_user_role"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users_roles")
