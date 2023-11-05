from dataclasses import dataclass
from uuid import UUID

from .base import RepoError


@dataclass(eq=False)
class IDNotFound(RepoError):
    id: UUID

    @property
    def title(self) -> str:
        return f"An calendar event with ID {self.id} not found"
