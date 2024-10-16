"""update tables

Revision ID: 2f0e6ca76dac
Revises: c0a3f6001efc
Create Date: 2024-10-11 20:19:58.565889

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2f0e6ca76dac"
down_revision: Union[str, None] = "c0a3f6001efc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "raspis",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ws_active", sa.Boolean(), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "messages", sa.Column("content", sa.String(length=1000), nullable=True)
    )
    op.drop_column("messages", "send_message")
    op.drop_index("raspi_id", table_name="users")
    op.create_foreign_key(
        None, "users", "raspis", ["raspi_id"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="foreignkey")
    op.create_index("raspi_id", "users", ["raspi_id"], unique=True)
    op.add_column(
        "messages", sa.Column("send_message", mysql.VARCHAR(length=1000), nullable=True)
    )
    op.drop_column("messages", "content")
    op.drop_table("raspis")
    # ### end Alembic commands ###
