"""Create Post table

Revision ID: 1812401db4b8
Revises: 
Create Date: 2022-01-24 19:25:32.212362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1812401db4b8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    '''Runs the commands for updating and creating table schemas'''
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))
    


def downgrade():
    '''Rolls back recent changes or drops table'''
    op.drop_table('posts')
