"""country now not required in city

Revision ID: 79517349331f
Revises: c36f28f7c67f
Create Date: 2024-12-01 03:15:17.268958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79517349331f'
down_revision: Union[str, None] = 'c36f28f7c67f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cities', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cities', 'country_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###