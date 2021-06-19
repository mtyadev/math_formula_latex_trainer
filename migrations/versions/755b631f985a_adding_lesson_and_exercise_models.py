"""Adding Lesson and Exercise models.

Revision ID: 755b631f985a
Revises: 7f8419b0c890
Create Date: 2021-06-19 16:59:18.992394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '755b631f985a'
down_revision = '7f8419b0c890'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('lesson', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lesson'], ['lesson.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exercise')
    op.drop_table('lesson')
    # ### end Alembic commands ###