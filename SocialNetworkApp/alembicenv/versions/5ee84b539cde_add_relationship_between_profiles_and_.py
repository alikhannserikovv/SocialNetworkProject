"""Add relationship between profiles and users

Revision ID: 5ee84b539cde
Revises: 
Create Date: 2025-02-12 19:34:03.576891

"""
from tkinter.constants import CASCADE
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ee84b539cde'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("users_profile_id_fkey", "users", type_="foreignkey")
    op.drop_constraint("profiles_user_id_fkey", "profiles", type_="foreignkey")
    op.create_foreign_key("users_profile_id_fkey", "users", "profiles",
                          ["profile_id"], ["id"], ondelete=CASCADE)
    op.create_foreign_key("profiles_user_id_fkey", "profiles", "users",
                          ["user_id"], ["id"], ondelete=CASCADE)

def downgrade() -> None:
    op.drop_constraint("users_profile_id_fkey", "users", type_="foreignkey")
    op.drop_constraint("profiles_user_id_fkey", "profiles", type_="foreignkey")
    op.create_foreign_key("users_profile_id_fkey", "users", "profiles",
                          ["profile_id"], ["id"])
    op.create_foreign_key("profiles_user_id_fkey", "profiles", "users",
                          ["user_id"], ["id"])
