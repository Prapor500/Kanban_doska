"""start

Revision ID: 1ebf78adc551
Revises: 28b888167d07
Create Date: 2025-11-06 22:05:33.154888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ebf78adc551'
down_revision: Union[str, None] = '28b888167d07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
