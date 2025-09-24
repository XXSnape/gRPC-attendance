"""empty message

Revision ID: 6cba3ce653b2
Revises: 9ecec2f63348
Create Date: 2025-09-24 21:29:04.159359

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6cba3ce653b2"
down_revision: Union[str, Sequence[str], None] = "9ecec2f63348"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "lessons",
        sa.Column("name", sa.String(), nullable=False),
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
            name=op.f("fk_lessons_department_id_departments"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lessons")),
        sa.UniqueConstraint(
            "name", "department_id", name="idx_uniq_name_department_id"
        ),
        sa.UniqueConstraint("name", name=op.f("uq_lessons_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("lessons")
