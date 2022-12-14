"""empty message

Revision ID: b6bb0a33966c
Revises: 802581c6a554
Create Date: 2022-09-21 22:10:15.237613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6bb0a33966c'
down_revision = '802581c6a554'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sched_notifications', sa.Column('test_message_key', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sched_notifications', 'test_message_key')
    # ### end Alembic commands ###
