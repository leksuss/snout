"""update_enum_values

Revision ID: 411aba9fb68f
Revises: 07664d738361
Create Date: 2024-11-22 21:50:34.084165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '411aba9fb68f'
down_revision: Union[str, None] = '07664d738361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE snapshotstatusenum RENAME VALUE 'HIDDEN' TO 'ACCESS_DENIED'")

def downgrade():
    op.execute("ALTER TYPE snapshotstatusenum RENAME VALUE 'ACCESS_DENIED' TO 'HIDDEN'")
