"""is_example_prj

Revision ID: ab78e304593e
Revises: e429a1fd8c61
Create Date: 2022-04-19 11:20:36.854249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ab78e304593e"
down_revision = "e429a1fd8c61"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_example", sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.drop_column("is_example")

    # ### end Alembic commands ###