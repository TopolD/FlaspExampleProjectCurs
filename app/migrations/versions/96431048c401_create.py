"""create

Revision ID: 96431048c401
Revises: 06fa9a2546ff
Create Date: 2025-05-20 19:37:41.957281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96431048c401'
down_revision: Union[str, None] = '06fa9a2546ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
