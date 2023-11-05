import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.adapters.db.main import get_engine, get_session_factory

from .config import API as APIConfig, Secret as SecretConfig, configure_logging, load_config_from_env
from .handlers import auth_router, calendar_events_router, jwt_exception_handler, users_router
from .providers import setup_providers

logger = logging.getLogger(__name__)


def init_api(
    engine: AsyncEngine,
    session_factory: async_sessionmaker[AsyncSession],
    secret_config: SecretConfig,
    debug: bool = __debug__,
) -> FastAPI:
    logger.info("Initializing API")

    app = FastAPI(
        debug=debug,
        title="Test Calendar Events API",
        version="0.1.0",
        default_response_class=ORJSONResponse,
    )

    app.add_exception_handler(JWTError, jwt_exception_handler)

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(calendar_events_router)

    setup_providers(app, engine, session_factory, secret_config)

    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    uvicorn_config = uvicorn.Config(
        app,
        host=api_config.host,
        port=api_config.port,
        log_level=logging.DEBUG,
    )

    server = uvicorn.Server(uvicorn_config)

    logger.info("Running API")

    await server.serve()


async def main() -> None:
    config = load_config_from_env()
    configure_logging(config.logging)

    logger.info("Starting application", extra={"config": config})

    engine = get_engine(config.db)
    session_factory = get_session_factory(engine)

    app = init_api(engine, session_factory, config.secret, config.api.debug)

    try:
        await run_api(app, config.api)
    finally:
        logger.info("Stopping application")

        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
