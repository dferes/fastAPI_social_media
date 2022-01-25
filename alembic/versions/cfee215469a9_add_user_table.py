"""Add user table

Revision ID: cfee215469a9
Revises: fb3dcbf1481c
Create Date: 2022-01-24 20:06:45.186391

"""
from time import timezone
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfee215469a9'
down_revision = 'fb3dcbf1481c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('username'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
