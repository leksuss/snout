"""Added unique constraint to Hashtag

Revision ID: 3fd98de5214d
Revises: b97f73f963d1
Create Date: 2024-12-11 23:36:55.654615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3fd98de5214d'
down_revision: Union[str, None] = 'b97f73f963d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publications_backup')
    op.create_unique_constraint('unique_hashtag_in_campaign', 'hashtags', ['name', 'campaign_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_hashtag_in_campaign', 'hashtags', type_='unique')
    op.create_table('publications_backup',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('type', postgresql.ENUM('CLIP', 'VIDEO', name='publtypeenum'), autoincrement=False, nullable=True),
    sa.Column('id_vk', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('date_published', sa.DATE(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
