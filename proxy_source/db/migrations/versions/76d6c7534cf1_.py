"""empty message

Revision ID: 76d6c7534cf1
Revises: 72ad361d8072
Create Date: 2021-09-05 14:52:15.063556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76d6c7534cf1'
down_revision = '72ad361d8072'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_proxy_ip', table_name='proxy')
    op.drop_index('ix_proxy_port', table_name='proxy')
    op.create_unique_constraint('ip_port_unique', 'proxy', ['ip', 'port'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ip_port_unique', 'proxy', type_='unique')
    op.create_index('ix_proxy_port', 'proxy', ['port'], unique=False)
    op.create_index('ix_proxy_ip', 'proxy', ['ip'], unique=False)
    # ### end Alembic commands ###
