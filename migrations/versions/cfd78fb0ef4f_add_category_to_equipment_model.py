"""Add category to Equipment model

Revision ID: cfd78fb0ef4f
Revises: 3e2d6061d6e9
Create Date: 2024-08-22 02:44:43.981909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd78fb0ef4f'
down_revision = '3e2d6061d6e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('image_file', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('details', sa.Text(), nullable=True))
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.alter_column('condition',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('owner',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=100),
               existing_nullable=True)
        batch_op.drop_index('ix_equipment_name')
        batch_op.drop_column('type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('equipment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.VARCHAR(length=64), nullable=True))
        batch_op.create_index('ix_equipment_name', ['name'], unique=False)
        batch_op.alter_column('owner',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('condition',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=64),
               nullable=True)
        batch_op.drop_column('details')
        batch_op.drop_column('image_file')
        batch_op.drop_column('category')

    # ### end Alembic commands ###
