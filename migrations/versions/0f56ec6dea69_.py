"""empty message

Revision ID: 0f56ec6dea69
Revises: e0fd41fa6ae8
Create Date: 2023-01-11 19:47:21.647013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f56ec6dea69'
down_revision = 'e0fd41fa6ae8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidateDB', 'password',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=60),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidateDB', 'password',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
