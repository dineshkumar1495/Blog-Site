"""Initial migration

Revision ID: 8712d8c94c7e
Revises: 
Create Date: 2023-07-08 16:20:47.652199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8712d8c94c7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=205), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('Users')
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog_posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', sa.VARCHAR(length=250), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author_id')

    op.create_table('Users',
    sa.Column('email', sa.VARCHAR(length=250), nullable=False),
    sa.Column('password', sa.VARCHAR(length=250), nullable=False),
    sa.Column('name', sa.VARCHAR(length=250), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
