"""empty message

Revision ID: 6fb37e905da3
Revises: 86b41bf9ad2a
Create Date: 2022-09-08 22:33:41.311405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fb37e905da3'
down_revision = '86b41bf9ad2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('posted', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'posted')
    # ### end Alembic commands ###