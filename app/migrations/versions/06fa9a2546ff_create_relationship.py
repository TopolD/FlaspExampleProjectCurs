"""create relationship  

Revision ID: 06fa9a2546ff
Revises: f1e231148c49
Create Date: 2025-05-20 19:36:55.336735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06fa9a2546ff'
down_revision: Union[str, None] = 'f1e231148c49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
