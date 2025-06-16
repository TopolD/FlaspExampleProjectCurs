"""create relationship user with booking 

Revision ID: f1e231148c49
Revises: 503df63ef685
Create Date: 2025-05-20 18:45:08.865625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e231148c49'
down_revision: Union[str, None] = '503df63ef685'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
