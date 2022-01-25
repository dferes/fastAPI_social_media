"""Add foreign key to posts table

Revision ID: b0a2ff9b73cc
Revises: cfee215469a9
Create Date: 2022-01-24 20:17:25.235803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0a2ff9b73cc'
down_revision = 'cfee215469a9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('username', sa.String(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['username'], remote_cols=['username'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'username')
