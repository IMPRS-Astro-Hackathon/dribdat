"""empty message

Revision ID: 84d8ce8453f3
Revises: 0c5ae11e7666
Create Date: 2022-09-17 08:04:21.745061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84d8ce8453f3'
down_revision = '0c5ae11e7666'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('hashtags', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'hashtags')
    # ### end Alembic commands ###
