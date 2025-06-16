"""changed

Revision ID: 86ba982fd23c
Revises: 96431048c401
Create Date: 2025-05-24 18:03:27.339993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86ba982fd23c'
down_revision: Union[str, None] = '96431048c401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
