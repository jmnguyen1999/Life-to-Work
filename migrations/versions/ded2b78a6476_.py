"""empty message

Revision ID: ded2b78a6476
Revises: 249ea132313c
Create Date: 2022-09-20 01:05:39.004235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ded2b78a6476'
down_revision = '249ea132313c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sched_notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('run_method', sa.String(length=64), nullable=False),
    sa.Column('message_key', sa.String(length=100), nullable=True),
    sa.Column('warning_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sched_notifications')
    # ### end Alembic commands ###