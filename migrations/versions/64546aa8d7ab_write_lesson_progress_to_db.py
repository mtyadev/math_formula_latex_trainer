"""write_lesson_progress_to_db

Revision ID: 64546aa8d7ab
Revises: 0f9832bb574c
Create Date: 2022-02-05 19:33:54.785633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64546aa8d7ab'
down_revision = '0f9832bb574c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_lesson_exercise_progress',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=False),
    sa.Column('times_shown', sa.Integer(), nullable=False),
    sa.Column('times_false', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lesson.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'lesson_id', 'exercise_id')
    )
    op.drop_column('exercise', 'lesson_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise', sa.Column('lesson_id', sa.INTEGER(), nullable=True))
    op.drop_table('user_lesson_exercise_progress')
    # ### end Alembic commands ###
