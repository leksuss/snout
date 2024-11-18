"""remove views field in publication

Revision ID: d7aced4ebd37
Revises: 333298b8f0ff
Create Date: 2024-11-18 20:48:02.919878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7aced4ebd37'
down_revision: Union[str, None] = '333298b8f0ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('publications', 'views')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('publications', sa.Column('views', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###