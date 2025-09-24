"""empty message

Revision ID: d9c5317b5568
Revises: 6cba3ce653b2
Create Date: 2025-09-24 21:29:49.190170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d9c5317b5568"
down_revision: Union[str, Sequence[str], None] = "6cba3ce653b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "groups",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "BACHELOR",
                "SPECIALTY",
                "MAGISTRACY",
                "POSTGRADUATE",
                name="groupenum",
            ),
            nullable=False,
        ),
        sa.Column("year_of_admission", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
            name=op.f("fk_groups_department_id_departments"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_groups")),
        sa.UniqueConstraint("name", "type", "year_of_admission", name="idx_uniq_group"),
        sa.UniqueConstraint("name", name=op.f("uq_groups_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("groups")
