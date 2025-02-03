"""change CarUser

Revision ID: b7113c32f3ac
Revises: 73edd08bfe71
Create Date: 2025-02-03 13:45:59.013820

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7113c32f3ac"
down_revision: Union[str, None] = "73edd08bfe71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("car_users", sa.Column("car_brand", sa.String(), nullable=True))
    op.add_column("car_users", sa.Column("car_model", sa.String(), nullable=True))
    op.add_column("car_users", sa.Column("car_year", sa.String(), nullable=True))
    op.drop_column("car_users", "info_about_car")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("car_users", sa.Column("info_about_car", sa.VARCHAR(), nullable=True))
    op.drop_column("car_users", "car_year")
    op.drop_column("car_users", "car_model")
    op.drop_column("car_users", "car_brand")
    # ### end Alembic commands ###
