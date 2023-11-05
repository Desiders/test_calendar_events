from dataclasses import dataclass


@dataclass(eq=False)
class AppException(Exception):
    """Base Exception"""

    @property
    def title(self) -> str:
        return "An app error occurred"


class UnexpectedError(AppException):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass
