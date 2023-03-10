"""empty message

Revision ID: d4946b3a0063
Revises: 1b085a952f48
Create Date: 2023-02-23 20:35:36.099455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4946b3a0063'
down_revision = '1b085a952f48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_constraint('todos_list_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'todolists', ['list_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('todos_list_id_fkey', 'todolists', ['list_id'], ['id'])

    # ### end Alembic commands ###
