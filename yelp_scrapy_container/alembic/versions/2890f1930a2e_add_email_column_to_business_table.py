"""add email column to business table

Revision ID: 2890f1930a2e
Revises: 
Create Date: 2020-06-11 13:06:47.666213

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import *


# revision identifiers, used by Alembic.
revision = '2890f1930a2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'business',
        sa.Column(
            'email',
            VARCHAR(255),
            )
        )


def downgrade():
    op.drop_column(
        'business',
        'email',
        )
