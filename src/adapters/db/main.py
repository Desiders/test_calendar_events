import orjson
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.config import Postgres as DBConfig


def get_engine(db_config: DBConfig) -> AsyncEngine:
    engine = create_async_engine(
        db_config.full_url,
        echo=True,
        echo_pool=db_config.echo,
        json_serializer=lambda data: orjson.dumps(data).decode(),
        json_deserializer=orjson.loads,
        pool_size=50,
    )
    return engine


def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    return session_factory
