"""Update Operating Hours Col From day_of_the_week to day_of_week and Add Constraint

Revision ID: 19087991d520
Revises: 78b485932a8b
Create Date: 2024-03-29 21:44:16.283622

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "19087991d520"
down_revision: Union[str, None] = "78b485932a8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "operating_hours", sa.Column("day_of_week", sa.Integer(), nullable=True)
    )
    op.drop_column("operating_hours", "day_of_the_week")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "operating_hours",
        sa.Column("day_of_the_week", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("operating_hours", "day_of_week")
    # ### end Alembic commands ###
