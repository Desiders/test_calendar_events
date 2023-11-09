import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.adapters.db.repositories import UserRepo
from src.adapters.jwt import JWTContext
from src.dtos import User
from src.providers import Stub

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": User,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
    response_class=ORJSONResponse,
    description="Get current user",
)
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
    user_repo: Annotated[UserRepo, Depends(Stub(UserRepo))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = credentials.credentials
    user_id = UUID(jwt_context.decode(token).sub)

    user = await user_repo.get_by_id(user_id)

    return user
