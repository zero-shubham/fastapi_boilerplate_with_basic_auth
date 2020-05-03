"""initial

Revision ID: 07c857af25ab
Revises: 
Create Date: 2020-04-05 11:08:15.917442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07c857af25ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.Column('user_type', sa.Enum('admin', 'user', name='usertypeenum'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tokens',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    op.drop_table('users')
    # ### end Alembic commands ###
