"""add foreign-key to posts table

Revision ID: c0dd1bcc00fa
Revises: 2f84899c7363
Create Date: 2021-11-30 16:59:06.404490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0dd1bcc00fa'
down_revision = '2f84899c7363'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('user_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_user_fkey',source_table="posts",
    referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete="CASCADE")

def downgrade():
    op.drop_constraint('posts_user_fkey',table_name="posts")
    op.drop_column('posts','user_id')
