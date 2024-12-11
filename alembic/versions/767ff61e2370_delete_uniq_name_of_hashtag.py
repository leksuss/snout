"""delete  uniq name of Hashtag

Revision ID: 767ff61e2370
Revises: 3fd98de5214d
Create Date: 2024-12-11 23:39:52.870908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '767ff61e2370'
down_revision: Union[str, None] = '3fd98de5214d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('hashtags_name_key', 'hashtags', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('hashtags_name_key', 'hashtags', ['name'])
    # ### end Alembic commands ###
