"""adjusting nullable for title in exercise model

Revision ID: ce1819de10b9
Revises: adda1eb5ea4c
Create Date: 2022-03-27 19:54:59.843429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce1819de10b9'
down_revision = 'adda1eb5ea4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise', sa.Column('title', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('exercise', 'title')
    # ### end Alembic commands ###
