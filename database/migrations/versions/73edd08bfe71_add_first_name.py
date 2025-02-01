"""add first_name

Revision ID: 73edd08bfe71
Revises: 71edd04f08d8
Create Date: 2025-01-31 16:43:08.348489

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "73edd08bfe71"
down_revision: Union[str, None] = "71edd04f08d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("first_name", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "first_name")
    # ### end Alembic commands ###
