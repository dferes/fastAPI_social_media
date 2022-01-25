"""Add a few more columns to the posts table

Revision ID: f5a988de5ae0
Revises: b0a2ff9b73cc
Create Date: 2022-01-24 20:25:23.563405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5a988de5ae0'
down_revision = 'b0a2ff9b73cc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='true'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
                                     server_default=sa.text('now()')))
                  


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
