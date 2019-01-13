"""add_cars_table

Revision ID: c1599f5e68b7
Revises: 
Create Date: 2019-01-13 03:42:39.578042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1599f5e68b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():op.create_table(
        'cars',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('colour', sa.String(), default='black'),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False))
    

def downgrade():
    op.drop_table('cars')

