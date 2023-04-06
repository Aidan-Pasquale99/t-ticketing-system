"""empty message

Revision ID: 8a23df8295f2
Revises: ca3a652d130e
Create Date: 2023-04-04 15:02:02.277084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a23df8295f2'
down_revision = 'ca3a652d130e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tickets')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tickets',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.VARCHAR(length=50), nullable=True),
    sa.Column('department', sa.VARCHAR(length=50), nullable=True),
    sa.Column('category', sa.VARCHAR(length=50), nullable=True),
    sa.Column('due_date', sa.DATE(), nullable=True),
    sa.Column('created_by', sa.VARCHAR(), nullable=True),
    sa.Column('updated_by', sa.VARCHAR(), nullable=True),
    sa.Column('created_date', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_date', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('name', sa.VARCHAR(length=150), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.email'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###