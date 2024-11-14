"""create models

Revision ID: 535d2f40167e
Revises: dd83904cc7df
Create Date: 2024-11-14 21:52:47.049003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '535d2f40167e'
down_revision: Union[str, None] = 'dd83904cc7df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('nickname', sa.String(), nullable=True),
    sa.Column('sex', sa.Enum('MALE', 'FEMALE', name='sexenum'), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('is_closed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['city_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vk_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('CLIP', 'VIDEO', name='publtypeenum'), nullable=False),
    sa.Column('views', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('publication_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('LIKE', 'COMMENT', name='activitytypeenum'), nullable=False),
    sa.ForeignKeyConstraint(['publication_id'], ['publications.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activities')
    op.drop_table('publications')
    op.drop_table('users')
    op.drop_table('cities')
    op.drop_table('countries')
    # ### end Alembic commands ###
