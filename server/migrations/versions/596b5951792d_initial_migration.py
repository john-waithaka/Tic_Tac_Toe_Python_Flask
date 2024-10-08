"""Initial migration

Revision ID: 596b5951792d
Revises: 
Create Date: 2024-09-10 09:09:09.023562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '596b5951792d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grid_size', sa.Integer(), nullable=False),
    sa.Column('player_x_id', sa.Integer(), nullable=False),
    sa.Column('player_o_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['player_o_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['player_x_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    op.drop_table('user')
    # ### end Alembic commands ###
