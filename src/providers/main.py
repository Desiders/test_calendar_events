from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.adapters.db.repositories import CalendarEventRepo, UserRepo
from src.adapters.db.uow import SQLAlchemyUoW
from src.adapters.hash import HashInCryptContext
from src.adapters.jwt import JWTContext
from src.config import Secret as SecretConfig

from .stub import Stub


async def get_sqlalchemy_uow(
    session_factory: Annotated[async_sessionmaker[AsyncSession], Depends(Stub(async_sessionmaker[AsyncSession]))]
) -> AsyncGenerator[SQLAlchemyUoW, None]:
    async with session_factory() as session:
        yield SQLAlchemyUoW(session)


def get_user_repo(
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))]
) -> Annotated[UserRepo, Depends(Stub(UserRepo))]:
    return UserRepo(uow.get_session())


def get_calendar_event_repo(
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))]
) -> Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))]:
    return CalendarEventRepo(uow.get_session())


def setup_providers(
    app: FastAPI,
    engine: AsyncEngine,
    session_factory: async_sessionmaker[AsyncSession],
    secret_config: SecretConfig,
) -> None:
    # Database providers
    app.dependency_overrides[Stub(AsyncEngine)] = lambda: engine
    app.dependency_overrides[Stub(async_sessionmaker[AsyncSession])] = lambda: session_factory
    app.dependency_overrides[Stub(SQLAlchemyUoW)] = get_sqlalchemy_uow
    app.dependency_overrides[Stub(UserRepo)] = get_user_repo
    app.dependency_overrides[Stub(CalendarEventRepo)] = get_calendar_event_repo

    hash_in_crypt_context = HashInCryptContext(schemes=["bcrypt"])

    # Hash providers
    app.dependency_overrides[Stub(HashInCryptContext)] = lambda: hash_in_crypt_context

    jwt_context = JWTContext(secret=secret_config.jwt)

    # JWT providers
    app.dependency_overrides[Stub(JWTContext)] = lambda: jwt_context
