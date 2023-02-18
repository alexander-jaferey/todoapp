"""added 'completed' column

Revision ID: 97feae1aeb80
Revises: 
Create Date: 2023-02-18 20:48:19.760913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97feae1aeb80'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=True))
        
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')
    op.alter_column('todos', 'completed', nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.drop_column('completed')

    # ### end Alembic commands ###
