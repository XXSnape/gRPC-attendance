"""empty message

Revision ID: 61e02cf787b7
Revises: cb90676788e1
Create Date: 2025-10-19 21:35:15.422599

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "61e02cf787b7"
down_revision: Union[str, Sequence[str], None] = "cb90676788e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "addresses",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_addresses")),
        sa.UniqueConstraint("name", name=op.f("uq_addresses_name")),
    )
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
        sa.UniqueConstraint(
            "name", name=op.f("uq_departments_name")
        ),
    )
    op.create_table(
        "specializations",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(length=20), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_specializations")
        ),
        sa.UniqueConstraint(
            "code", name=op.f("uq_specializations_code")
        ),
        sa.UniqueConstraint(
            "name", name=op.f("uq_specializations_name")
        ),
    )
    op.create_table(
        "users",
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column(
            "gender",
            sa.Enum(
                "MALE",
                "FEMALE",
                name="genderenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(
        op.f("ix_users_email"), "users", ["email"], unique=True
    )
    op.create_table(
        "administrators",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["users.id"],
            name=op.f("fk_administrators_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_administrators")
        ),
    )
    op.create_table(
        "audiences",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["addresses.id"],
            name=op.f("fk_audiences_address_id_addresses"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audiences")),
        sa.UniqueConstraint(
            "name", "address_id", name="idx_uniq_name_address"
        ),
    )
    op.create_table(
        "groups",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "level",
            sa.Enum(
                "BACHELOR",
                "SPECIALIST",
                "MASTER",
                "POSTGRADUATE",
                name="levelenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("department_id", sa.UUID(), nullable=False),
        sa.Column("specialization_id", sa.UUID(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["specialization_id"],
            ["specializations.id"],
            name=op.f("fk_groups_specialization_id_specializations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_groups")),
        sa.UniqueConstraint(
            "level",
            "department_id",
            "specialization_id",
            name="idx_uniq_group",
        ),
        sa.UniqueConstraint("name", name=op.f("uq_groups_name")),
    )
    op.create_table(
        "lessons",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("department_id", sa.UUID(), nullable=False),
        sa.Column(
            "on_schedule",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column("type", sa.String(), nullable=False),
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
        sa.UniqueConstraint("name", name=op.f("uq_lessons_name")),
    )
    op.create_table(
        "students",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("personal_number", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["users.id"],
            name=op.f("fk_students_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_students")),
        sa.UniqueConstraint(
            "personal_number",
            name=op.f("uq_students_personal_number"),
        ),
    )
    op.create_table(
        "teachers",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("department_id", sa.UUID(), nullable=False),
        sa.Column("is_eldest", sa.Boolean(), nullable=False),
        sa.Column(
            "rank",
            sa.Enum(
                "DOCENT",
                "PROFESSOR",
                name="rankenum",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column(
            "degree",
            sa.Enum(
                "CANDIDATE_OF_SCIENCES",
                "DOCTOR_OF_SCIENCES",
                name="degreeenum",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
            name=op.f("fk_teachers_department_id_departments"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["users.id"],
            name=op.f("fk_teachers_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teachers")),
    )
    op.create_table(
        "group_numbers",
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("year_of_admission", sa.Integer(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "number >= 1",
            name=op.f("ck_group_numbers_idx_group_number"),
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk_group_numbers_group_id_groups"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_group_numbers")),
        sa.UniqueConstraint(
            "group_id",
            "number",
            "year_of_admission",
            name="idx_uniq_number_group",
        ),
    )
    op.create_table(
        "lessons_types",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("kind", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["lessons.id"],
            name=op.f("fk_lessons_types_id_lessons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lessons_types")),
    )
    op.create_table(
        "schedules",
        sa.Column(
            "type_of_lesson",
            sa.Enum(
                "LECTURE",
                "PRACTICAL",
                "LAB",
                "EXAM",
                "TEST",
                name="typeoflessonenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.UUID(), nullable=False),
        sa.Column("audience_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "number >= 1 AND number <= 6",
            name=op.f("ck_schedules_idx_number"),
        ),
        sa.ForeignKeyConstraint(
            ["audience_id"],
            ["audiences.id"],
            name=op.f("fk_schedules_audience_id_audiences"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
            name=op.f("fk_schedules_lesson_id_lessons"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedules")),
        sa.UniqueConstraint(
            "type_of_lesson",
            "date",
            "number",
            "lesson_id",
            "audience_id",
            name="idx_uniq_schedule",
        ),
    )
    op.create_table(
        "groups_schedules",
        sa.Column(
            "subgroup_number",
            sa.Integer(),
            server_default=sa.text("NULL"),
            nullable=True,
        ),
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("schedule_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "subgroup_number IS NULL or (subgroup_number >= 1 AND subgroup_number <= 2)",
            name=op.f("ck_groups_schedules_idx_subgroup"),
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["group_numbers.id"],
            name=op.f("fk_groups_schedules_group_id_group_numbers"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
            name=op.f("fk_groups_schedules_schedule_id_schedules"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_groups_schedules")
        ),
        sa.UniqueConstraint(
            "subgroup_number",
            "group_id",
            "schedule_id",
            name="idx_uniq_subgroup_schedule",
        ),
    )
    op.create_table(
        "schedule_exceptions",
        sa.Column("schedule_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
            name=op.f(
                "fk_schedule_exceptions_schedule_id_schedules"
            ),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_schedule_exceptions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_schedule_exceptions")
        ),
    )
    op.create_table(
        "students_groups",
        sa.Column("student_id", sa.UUID(), nullable=False),
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column(
            "form_of_education",
            sa.Enum(
                "FULL_TIME",
                "PART_TIME",
                "DISTANCE",
                name="formofeducationenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "type_of_refund",
            sa.Enum(
                "STATE_FUNDED",
                "OVER_PLANNED",
                name="typeofrefundenum",
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
            ["group_numbers.id"],
            name=op.f("fk_students_groups_group_id_group_numbers"),
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
        sa.UniqueConstraint(
            "student_id", "group_id", name="idx_uniq_user_group"
        ),
    )
    op.create_table(
        "teachers_schedules",
        sa.Column("schedule_id", sa.UUID(), nullable=False),
        sa.Column("teacher_id", sa.UUID(), nullable=False),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v7()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
            name=op.f("fk_teachers_schedules_schedule_id_schedules"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["teachers.id"],
            name=op.f("fk_teachers_schedules_teacher_id_teachers"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_teachers_schedules")
        ),
        sa.UniqueConstraint(
            "teacher_id",
            "schedule_id",
            name="idx_uniq_teacher_schedule",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("teachers_schedules")
    op.drop_table("students_groups")
    op.drop_table("schedule_exceptions")
    op.drop_table("groups_schedules")
    op.drop_table("schedules")
    op.drop_table("lessons_types")
    op.drop_table("group_numbers")
    op.drop_table("teachers")
    op.drop_table("students")
    op.drop_table("lessons")
    op.drop_table("groups")
    op.drop_table("audiences")
    op.drop_table("administrators")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("specializations")
    op.drop_table("departments")
    op.drop_table("addresses")
