"""create users table

Revision ID: 2f32e4589265
Revises: 
Create Date: 2024-01-20 17:03:32.607253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f32e4589265'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
