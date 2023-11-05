import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import ORJSONResponse
from uuid6 import uuid7

from src.adapters.db.repositories import UserRepo
from src.adapters.db.uow import SQLAlchemyUoW
from src.adapters.hash import HashInCryptContext
from src.adapters.jwt import JWTContext
from src.dtos import Token, User
from src.exceptions import UserUsernameNotFound
from src.providers import Stub

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {
            "model": Token,
            "description": "Login successful",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
    response_class=ORJSONResponse,
    description="Login to the API",
)
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_repo: Annotated[UserRepo, Depends(Stub(UserRepo))],
    hash_in_crypt_context: Annotated[HashInCryptContext, Depends(Stub(HashInCryptContext))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
) -> Token:
    try:
        user = await user_repo.get_by_username(username)
    except UserUsernameNotFound as exc:
        logger.debug("User not found", extra={"username": username})

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc

    if not hash_in_crypt_context.verify(password, user.hashed_password):
        logger.debug("Invalid credentials", extra={"username": username})

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = jwt_context.encode(sub=str(user.id))

    token = Token(access_token, token_type="bearer")

    return token


@router.post(
    "/register",
    responses={
        status.HTTP_201_CREATED: {
            "model": Token,
            "description": "Registration successful",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid credentials",
        },
    },
    response_class=ORJSONResponse,
    description="Register to the API",
)
async def register(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    user_repo: Annotated[UserRepo, Depends(Stub(UserRepo))],
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))],
    hash_in_crypt_context: Annotated[HashInCryptContext, Depends(Stub(HashInCryptContext))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
) -> Token:
    try:
        await user_repo.get_by_username(username)
    except UserUsernameNotFound:
        pass
    else:
        logger.debug("Username already exists", extra={"username": username})

        await uow.rollback()

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = hash_in_crypt_context.hash(password)

    user_id = uuid7()

    await user_repo.add(User(id=user_id, username=username, hashed_password=hashed_password))
    await uow.commit()

    logger.debug("User registered", extra={"username": username})

    access_token = jwt_context.encode(sub=str(user_id))

    token = Token(access_token, token_type="bearer")

    return token
