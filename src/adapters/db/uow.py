from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUoW:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def get_session(self) -> AsyncSession:
        return self._session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
