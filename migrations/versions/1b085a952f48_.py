"""empty message

Revision ID: 1b085a952f48
Revises: 5122f3750822
Create Date: 2023-02-23 19:52:50.612190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b085a952f48'
down_revision = '5122f3750822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todolists', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todolists', schema=None) as batch_op:
        batch_op.drop_column('completed')

    # ### end Alembic commands ###