"""add last few columns to the posts table

Revision ID: 748406f37c0a
Revises: c0dd1bcc00fa
Create Date: 2021-11-30 17:10:26.812407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '748406f37c0a'
down_revision = 'c0dd1bcc00fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False)),
    op.add_column('posts',sa.Column('publish',sa.Boolean(),nullable=False,server_default="TRUE"),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),
    nullable=False,server_default=sa.text('NOW()')),)


def downgrade():
    op.drop_column('posts','content')
    op.drop_column('posts','publish')
    op.drop_column('posts','created_at')
