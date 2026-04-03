"""add embedding columns for pgvector

Revision ID: 371870bcf3d4
Revises: 1bb3321256d7
Create Date: 2026-04-01 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "371870bcf3d4"
down_revision: Union[str, Sequence[str], None] = "1bb3321256d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add embedding columns for pgvector."""
    # Add embedding column to articles table
    op.add_column(
        "articles",
        sa.Column("embedding", sa.String(), nullable=True),
    )

    # Add embedding column to comments table
    op.add_column(
        "comments",
        sa.Column("embedding", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema - Remove embedding columns."""
    # Drop embedding column from comments table
    op.drop_column("comments", "embedding")

    # Drop embedding column from articles table
    op.drop_column("articles", "embedding")
