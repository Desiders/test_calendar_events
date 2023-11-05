"""init_tables

Revision ID: 8763fd272bc1
Revises: 51bdaf978507
Create Date: 2023-11-04 14:48:34.872536

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8763fd272bc1"
down_revision = "51bdaf978507"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuid_generate_v7()"), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), server_default=sa.text("NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )
    op.create_table(
        "calendar_events",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuid_generate_v7()"), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), server_default=sa.text("NULL"), nullable=True),
        sa.Column("is_private", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("start_date", sa.DateTime(), server_default=sa.text("NULL"), nullable=True),
        sa.Column("end_date", sa.DateTime(), server_default=sa.text("NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_calendar_events_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_calendar_events")),
    )


def downgrade() -> None:
    op.drop_table("calendar_events")
    op.drop_table("users")
