"""Add stats fields to User model

Revision ID: 3acfd87a5ade
Revises: a162f2db525b
Create Date: 2024-09-11 02:13:45.258815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '3acfd87a5ade'
down_revision = 'a162f2db525b'
branch_labels = None
depends_on = None


def upgrade():
    # Bind the connection to check existing columns
    conn = op.get_bind()
    inspector = inspect(conn)

    # Fetch all columns in the 'game' table
    columns = [column['name'] for column in inspector.get_columns('game')]

    # Only add 'current_turn' if it doesn't exist already
    if 'current_turn' not in columns:
        op.add_column('game', sa.Column('current_turn', sa.String(length=1), nullable=True))

def downgrade():
    # Add a corresponding downgrade if necessary
    op.drop_column('game', 'current_turn')
