"""empty message

Revision ID: 72ad361d8072
Revises: 0c8ab1c52849
Create Date: 2021-09-05 14:36:08.938766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '72ad361d8072'
down_revision = '0c8ab1c52849'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proxy',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('protocol', sa.Enum('http', 'https', name='protocolenum', native_enum=False), nullable=False),
    sa.Column('ip', postgresql.INET(), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('user', sa.Unicode(), nullable=True),
    sa.Column('password', sa.Unicode(), nullable=True),
    sa.Column('source', sa.Enum('best_proxies', name='sourceenum', native_enum=False), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_proxy'))
    )
    op.create_index(op.f('ix_proxy_created_at'), 'proxy', ['created_at'], unique=False)
    op.create_index(op.f('ix_proxy_deleted_at'), 'proxy', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_proxy_id'), 'proxy', ['id'], unique=False)
    op.create_index(op.f('ix_proxy_ip'), 'proxy', ['ip'], unique=False)
    op.create_index(op.f('ix_proxy_password'), 'proxy', ['password'], unique=False)
    op.create_index(op.f('ix_proxy_port'), 'proxy', ['port'], unique=False)
    op.create_index(op.f('ix_proxy_protocol'), 'proxy', ['protocol'], unique=False)
    op.create_index(op.f('ix_proxy_source'), 'proxy', ['source'], unique=False)
    op.create_index(op.f('ix_proxy_user'), 'proxy', ['user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_proxy_user'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_source'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_protocol'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_port'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_password'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_ip'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_id'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_deleted_at'), table_name='proxy')
    op.drop_index(op.f('ix_proxy_created_at'), table_name='proxy')
    op.drop_table('proxy')
    # ### end Alembic commands ###
