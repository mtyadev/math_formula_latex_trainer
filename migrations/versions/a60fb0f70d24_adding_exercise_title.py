"""adding exercise title

Revision ID: a60fb0f70d24
Revises: 64546aa8d7ab
Create Date: 2022-03-26 21:21:21.171493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a60fb0f70d24'
down_revision = '64546aa8d7ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise', sa.Column('title', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercise', 'title')
    # ### end Alembic commands ###
