"""Add quantity field to Equipment model

Revision ID: 34c158261609
Revises: 92a45e39d3d5
Create Date: 2024-09-02 00:54:55.492839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c158261609'
down_revision = '92a45e39d3d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
