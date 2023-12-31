from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CalendarEvent:
    id: UUID
    user_id: UUID
    title: str
    is_private: bool
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
