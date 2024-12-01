"""add is_banned, is_deleted for user

Revision ID: c36f28f7c67f
Revises: 411aba9fb68f
Create Date: 2024-12-01 02:54:31.272436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c36f28f7c67f'
down_revision: Union[str, None] = '411aba9fb68f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('screen_name', sa.String(length=255), nullable=True))
    op.add_column('users', sa.Column('is_banned', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=True))
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'is_deleted')
    op.drop_column('users', 'is_banned')
    op.drop_column('users', 'screen_name')
    # ### end Alembic commands ###