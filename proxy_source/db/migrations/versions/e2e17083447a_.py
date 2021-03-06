"""empty message

Revision ID: e2e17083447a
Revises: e7e01ff1f6c7
Create Date: 2021-09-28 21:14:30.702142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2e17083447a'
down_revision = 'e7e01ff1f6c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('proxy', sa.Column('is_active', sa.Boolean(), server_default='False', nullable=False))
    op.create_index(op.f('ix_proxy_is_active'), 'proxy', ['is_active'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_proxy_is_active'), table_name='proxy')
    op.drop_column('proxy', 'is_active')
    # ### end Alembic commands ###
