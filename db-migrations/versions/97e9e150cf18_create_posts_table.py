"""create posts table

Revision ID: 97e9e150cf18
Revises: 
Create Date: 2021-11-30 15:27:27.029113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97e9e150cf18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
        sa.Column('title',sa.String(),nullable=False)
    )


def downgrade():
    op.drop_table("posts")
