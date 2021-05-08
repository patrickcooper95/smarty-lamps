"""add program columns

Revision ID: 45892d6e28d4
Revises: 0f11ba2f4215
Create Date: 2021-05-08 17:10:54.224676

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = '45892d6e28d4'
down_revision = '0f11ba2f4215'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("colors") as batch_op:
        batch_op.add_column(Column('dynamic', String()))
        batch_op.add_column(Column('callable_path', String()))


def downgrade():
    with op.batch_alter_table("colors") as batch_op:
        batch_op.drop_column('dynamic')
        batch_op.drop_column('callable_path')
