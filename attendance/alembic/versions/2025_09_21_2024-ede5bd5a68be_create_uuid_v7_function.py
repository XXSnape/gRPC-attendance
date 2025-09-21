"""create uuid v7 function

Revision ID: ede5bd5a68be
Revises:
Create Date: 2025-09-21 20:24:40.732142

"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ede5bd5a68be"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

uuid_v7_functions = (
    Path(
        context.config.get_section_option(
            "extra",
            "functions.dir",
        )
    )
    / "uuid_v7"
)


def upgrade() -> None:
    op.execute(
        (uuid_v7_functions / "upgrade.sql").read_text(),
    )


def downgrade() -> None:
    op.execute(
        (uuid_v7_functions / "downgrade.sql").read_text(),
    )
