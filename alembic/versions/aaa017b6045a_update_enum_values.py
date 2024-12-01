"""update_enum_values

Revision ID: aaa017b6045a
Revises: 79517349331f
Create Date: 2024-12-01 03:44:41.641287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaa017b6045a'
down_revision: Union[str, None] = '79517349331f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE sexenum ADD VALUE 'UNKNOWN'")

def downgrade():
    pass