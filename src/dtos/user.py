from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    hashed_password: str
    deleted_at: datetime | None = None
