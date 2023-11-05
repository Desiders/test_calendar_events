from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7, server_default=sa.func.uuid_generate_v7())
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    deleted_at: Mapped[datetime | None] = mapped_column(default=None, server_default=sa.Null())
