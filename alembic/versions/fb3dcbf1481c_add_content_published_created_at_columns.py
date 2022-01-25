"""Add content column

Revision ID: fb3dcbf1481c
Revises: 1812401db4b8
Create Date: 2022-01-24 19:46:57.988627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb3dcbf1481c'
down_revision = '1812401db4b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')

