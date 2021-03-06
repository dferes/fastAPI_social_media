"""auto-generated votes table

Revision ID: ec4b0917d7df
Revises: f5a988de5ae0
Create Date: 2022-01-24 21:04:34.601274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4b0917d7df'
down_revision = 'f5a988de5ae0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['username'], ['users.username'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('username', 'post_id')
    )
    op.alter_column('posts', 'published',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('true'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'published',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('true'))
    op.drop_table('votes')
    # ### end Alembic commands ###
