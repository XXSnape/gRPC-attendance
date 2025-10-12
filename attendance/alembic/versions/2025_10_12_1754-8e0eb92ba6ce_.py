"""empty message

Revision ID: 8e0eb92ba6ce
Revises: 43443837afb2
Create Date: 2025-10-12 17:54:42.787227

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "8e0eb92ba6ce"
down_revision: Union[str, Sequence[str], None] = "43443837afb2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "students_groups",
        sa.Column("student_id", sa.UUID(), nullable=False),
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("year_of_admission", sa.Integer(), nullable=False),
        sa.Column(
            "form_of_education",
            sa.Enum(
                "FULL_TIME",
                "PART_TIME",
                "DISTANCE",
                name="formofeducationenum2",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "type_of_refund",
            sa.Enum(
                "STATE_FUNDED",
                "OVER_PLANNED",
                name="typeofrefundenum2",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "is_prefect",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_students_groups_group_id_groups"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            name=op.f("fk_students_groups_student_id_students"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_students_groups")
        ),
    )
    op.drop_table("users_groups")
    op.drop_table("teachers_departments")
    op.add_column(
        "teachers_schedules",
        sa.Column("teacher_id", sa.UUID(), nullable=False),
    )
    op.drop_constraint(
        op.f("idx_uniq_teacher_schedule"),
        "teachers_schedules",
        type_="unique",
    )
    op.create_unique_constraint(
        "idx_uniq_teacher_schedule",
        "teachers_schedules",
        ["teacher_id", "schedule_id"],
    )
    op.drop_constraint(
        op.f("fk_teachers_schedules_user_id_users"),
        "teachers_schedules",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_teachers_schedules_teacher_id_teachers"),
        "teachers_schedules",
        "teachers",
        ["teacher_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("teachers_schedules", "user_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "teachers_schedules",
        sa.Column(
            "user_id", sa.UUID(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(
        op.f("fk_teachers_schedules_teacher_id_teachers"),
        "teachers_schedules",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("fk_teachers_schedules_user_id_users"),
        "teachers_schedules",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "idx_uniq_teacher_schedule",
        "teachers_schedules",
        type_="unique",
    )
    op.create_unique_constraint(
        op.f("idx_uniq_teacher_schedule"),
        "teachers_schedules",
        ["user_id", "schedule_id"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("teachers_schedules", "teacher_id")
    op.create_table(
        "teachers_departments",
        sa.Column(
            "user_id", sa.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "department_id",
            sa.UUID(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
            name=op.f(
                "fk_teachers_departments_department_id_departments"
            ),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_teachers_departments_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_teachers_departments")
        ),
        sa.UniqueConstraint(
            "user_id",
            "department_id",
            name=op.f("idx_uniq_teacher_department"),
            postgresql_include=[],
            postgresql_nulls_not_distinct=False,
        ),
    )
    op.create_table(
        "users_groups",
        sa.Column(
            "user_id", sa.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "group_id",
            sa.UUID(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "year_of_admission",
            sa.INTEGER(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "form_of_education",
            postgresql.ENUM(
                "FULL_TIME",
                "PART_TIME",
                "DISTANCE",
                name="formofeducationenum",
                create_type=False,
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "type_of_refund",
            postgresql.ENUM(
                "STATE_FUNDED",
                "OVER_PLANNED",
                name="typeofrefundenum",
                create_type=False,
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "is_prefect",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_users_groups_group_id_groups"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_users_groups_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users_groups")),
        sa.UniqueConstraint(
            "user_id",
            "group_id",
            "year_of_admission",
            name=op.f("idx_uniq_user_group"),
            postgresql_include=[],
            postgresql_nulls_not_distinct=False,
        ),
    )
    op.drop_table("students_groups")
