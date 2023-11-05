from dataclasses import dataclass
from uuid import UUID

from .base import RepoError


@dataclass(eq=False)
class IDNotFound(RepoError):
    id: UUID

    @property
    def title(self) -> str:
        return f"A user with ID {self.id} not found"


@dataclass(eq=False)
class UsernameNotFound(RepoError):
    username: str

    @property
    def title(self) -> str:
        return f"A user with username {self.username} not found"
