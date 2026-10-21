"""crear tabla especificaciones equipo

Revision ID: a7850771cb37
Revises: 0f8953e6c716
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a7850771cb37"
down_revision: Union[str, Sequence[str], None] = "0f8953e6c716"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass