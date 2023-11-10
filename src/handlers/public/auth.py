import logging
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.adapters.jwt import JWTContext
from src.config import Static as StaticConfig
from src.providers import Stub

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get(
    "/login",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "text/html": {},
            },
            "description": "Login page",
        },
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "content": {
                "text/html": {},
            },
            "description": "Redirect to home page if user already logged in",
        },
    },
    response_class=HTMLResponse,
)
def login(
    static_config: Annotated[StaticConfig, Depends(Stub(StaticConfig))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    token: Annotated[
        str | None,
        Cookie(
            alias="ACCESS_TOKEN",
            description="Access token",
        ),
    ] = None,
):
    if token and jwt_context.verify(token):
        logger.debug("User already logged in and redirected to home page")

        return RedirectResponse("/")

    return HTMLResponse(
        open(static_config.path / "login.html").read(),
    )


@router.get(
    "/register",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "text/html": {},
            },
            "description": "Registration page",
        },
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "content": {
                "text/html": {},
            },
            "description": "Redirect to home page if user already logged in",
        },
    },
    response_class=HTMLResponse,
)
def register(
    static_config: Annotated[StaticConfig, Depends(Stub(StaticConfig))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    token: Annotated[
        str | None,
        Cookie(
            alias="ACCESS_TOKEN",
            description="Access token",
        ),
    ] = None,
):
    if token and jwt_context.verify(token):
        logger.debug("User already logged in and redirected to home page")

        return RedirectResponse("/")

    return HTMLResponse(
        open(static_config.path / "registration.html").read(),
    )


@router.get(
    "/logout",
    responses={
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "content": {
                "text/html": {},
            },
            "description": "Redirect to login page",
        },
    },
)
def logout(
    token: Annotated[
        str | None,
        Cookie(
            alias="ACCESS_TOKEN",
            description="Access token",
        ),
    ] = None,
):
    response = RedirectResponse("/auth/login")

    if token:
        response.delete_cookie("ACCESS_TOKEN")

    return response
