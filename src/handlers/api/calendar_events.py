import logging
from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from uuid6 import uuid7

from src.adapters.db.repositories import CalendarEventRepo
from src.adapters.db.uow import SQLAlchemyUoW
from src.adapters.jwt import JWTContext
from src.dtos import CalendarEvent
from src.exceptions import CalendarEventIDNotFound
from src.providers import Stub

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/calendar-events",
    tags=["calendar-events"],
)


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {
            "model": UUID,
            "description": "Calendar event created. Returns calendar event id",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
    description="Create calendar event",
)
async def create_calendar_event(
    calendar_event_repo: Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))],
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
    title: Annotated[str, Form()],
    is_private: Annotated[bool, Form()] = True,
    description: Annotated[str | None, Form()] = None,
    start_date: Annotated[datetime | None, Form()] = None,
    end_date: Annotated[datetime | None, Form()] = None,
) -> UUID:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = credentials.credentials

    user_id = UUID(jwt_context.decode(token).sub)
    calendar_event_id = uuid7()

    await calendar_event_repo.add(
        CalendarEvent(
            id=calendar_event_id,
            user_id=user_id,
            title=title,
            is_private=is_private,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
    )
    await uow.commit()

    return calendar_event_id


@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {
            "model": CalendarEvent,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Calendar event is private. You can't access it.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Calendar event not found",
        },
    },
    response_class=ORJSONResponse,
    description="Get calendar event by id",
)
async def get_calendar_event_by_id(
    id: UUID,
    calendar_event_repo: Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
) -> CalendarEvent:
    try:
        calendar_event = await calendar_event_repo.get_by_id(id)
    except CalendarEventIDNotFound as exc:
        logger.debug("Calendar event not found", extra={"id": id})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found") from exc

    token = None if credentials is None else credentials.credentials

    if calendar_event.is_private and (token is None or calendar_event.user_id != UUID(jwt_context.decode(token).sub)):
        logger.debug("Calendar event is private", extra={"id": id, "owned_user_id": calendar_event.user_id})

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Calendar event is private. You can't access it."
        )

    return calendar_event


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": list[CalendarEvent],
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
    response_class=ORJSONResponse,
    description="Get current user calendar events",
)
async def get_calendar_events(
    calendar_event_repo: Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
) -> list[CalendarEvent]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = credentials.credentials
    user_id = UUID(jwt_context.decode(token).sub)

    calendar_events = await calendar_event_repo.get_by_user_id(user_id)

    return calendar_events


@router.delete(
    "/{id}",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Calendar event deleted",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Calendar event is not owned by you. You can't delete it.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Calendar event not found",
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete calendar event by id",
)
async def delete_calendar_event_by_id(
    id: UUID,
    calendar_event_repo: Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))],
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
) -> None:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    try:
        calendar_event = await calendar_event_repo.get_by_id(id)
    except CalendarEventIDNotFound as exc:
        logger.debug("Calendar event not found", extra={"id": id})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found") from exc

    token = credentials.credentials

    if calendar_event.user_id != UUID(jwt_context.decode(token).sub):
        logger.debug("Calendar event is not owned by you", extra={"id": id, "owned_user_id": calendar_event.user_id})

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Calendar event is not owned by you. You can't delete it."
        )

    await calendar_event_repo.delete_by_id(id)
    await uow.commit()


@router.put(
    "/{id}",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Calendar event updated",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Calendar event is not owned by you. You can't update it.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Calendar event not found",
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update calendar event by id",
)
async def update_calendar_event_by_id(
    calendar_event_repo: Annotated[CalendarEventRepo, Depends(Stub(CalendarEventRepo))],
    uow: Annotated[SQLAlchemyUoW, Depends(Stub(SQLAlchemyUoW))],
    jwt_context: Annotated[JWTContext, Depends(Stub(JWTContext))],
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))],
    id: UUID,
    title: Annotated[str, Form()],
    is_private: Annotated[bool, Form()] = True,
    description: Annotated[str | None, Form()] = None,
    start_date: Annotated[datetime | None, Form()] = None,
    end_date: Annotated[datetime | None, Form()] = None,
) -> None:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    try:
        calendar_event = await calendar_event_repo.get_by_id(id)
    except CalendarEventIDNotFound as exc:
        logger.debug("Calendar event not found", extra={"id": id})

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calendar event not found") from exc

    token = credentials.credentials

    if calendar_event.user_id != UUID(jwt_context.decode(token).sub):
        logger.debug("Calendar event is not owned by you", extra={"id": id, "owned_user_id": calendar_event.user_id})

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Calendar event is not owned by you. You can't update it."
        )

    await calendar_event_repo.update(
        CalendarEvent(
            id=id,
            user_id=calendar_event.user_id,
            title=title,
            is_private=is_private,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
    )
    await uow.commit()
