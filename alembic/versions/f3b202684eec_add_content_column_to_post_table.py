"""add content column to post table

Revision ID: f3b202684eec
Revises: b95a0bb9eb78
Create Date: 2024-10-16 13:23:04.801140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b202684eec'
down_revision: Union[str, None] = 'b95a0bb9eb78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
