"""empty message

Revision ID: 13796bbe4df2
Revises: 
Create Date: 2021-03-22 21:48:31.734766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13796bbe4df2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('profile', sa.String(length=180), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('addproduct',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=True),
    sa.Column('discount', sa.Integer(), nullable=True),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('colors', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('image_1', sa.String(length=150), nullable=False),
    sa.Column('image_2', sa.String(length=150), nullable=False),
    sa.Column('image_3', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('addproduct')
    op.drop_table('user')
    op.drop_table('category')
    op.drop_table('brand')
    # ### end Alembic commands ###
