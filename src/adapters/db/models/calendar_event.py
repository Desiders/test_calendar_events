from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from .base import TimedBaseModel


class CalendarEvent(TimedBaseModel):
    __tablename__ = "calendar_events"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7, server_default=sa.func.uuid_generate_v7())
    user_id: Mapped[UUID] = mapped_column(sa.ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column(default=None, server_default=sa.Null())
    is_private: Mapped[bool] = mapped_column(default=True, server_default=sa.true())
    start_date: Mapped[datetime | None] = mapped_column(default=None, server_default=sa.Null())
    end_date: Mapped[datetime | None] = mapped_column(default=None, server_default=sa.Null())
