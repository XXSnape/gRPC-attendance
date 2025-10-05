"""create uuid v7 function

Revision ID: cb90676788e1
Revises:
Create Date: 2025-10-05 15:03:09.135394

"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cb90676788e1"
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
