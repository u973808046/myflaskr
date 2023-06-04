"""empty message

Revision ID: 238e74d92d6a
Revises: fe4c84d572b8
Create Date: 2023-06-03 18:52:29.922874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '238e74d92d6a'
down_revision = 'fe4c84d572b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.NullType(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    # ### end Alembic commands ###
