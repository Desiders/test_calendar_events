from uuid import UUID

from sqlalchemy import select

from src.adapters.db.converters import user_dto_to_model, user_model_to_dto
from src.adapters.db.models import User
from src.dtos import User as UserDTO
from src.exceptions import UserIDNotFound, UserUsernameNotFound

from .base import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo):
    async def get_by_id(self, id: UUID) -> UserDTO:
        user = await self._session.scalar(select(User).filter(User.id == id))

        if user is None:
            raise UserIDNotFound(id)

        return user_model_to_dto(user)

    async def get_by_username(self, username: str) -> UserDTO:
        user = await self._session.scalar(select(User).filter(User.username == username))

        if user is None:
            raise UserUsernameNotFound(username)

        return user_model_to_dto(user)

    async def add(self, user: UserDTO) -> None:
        self._session.add(user_dto_to_model(user))

        await self._session.flush()
