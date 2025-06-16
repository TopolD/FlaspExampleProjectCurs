"""datetime > date

Revision ID: a24910279025
Revises: 86ba982fd23c
Create Date: 2025-05-29 14:49:27.085819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a24910279025'
down_revision: Union[str, None] = '86ba982fd23c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
