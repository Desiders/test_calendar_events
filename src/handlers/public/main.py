import logging
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.adapters.jwt import JWTContext
from src.config import Static as StaticConfig
from src.providers import Stub

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["main"],
)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "content": {
                "text/html": {},
            },
            "description": "Main page",
        },
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "content": {
                "text/html": {},
            },
            "description": "Redirect to register page",
        },
    },
    response_class=HTMLResponse,
)
def main_page(
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
    if not token or not jwt_context.verify(token):
        return RedirectResponse("/auth/register")

    return HTMLResponse(
        open(static_config.path / "index.html").read(),
    )
