from src import dtos

from . import models


def user_model_to_dto(user: models.User) -> dtos.User:
    return dtos.User(
        id=user.id,
        username=user.username,
        hashed_password=user.hashed_password,
        deleted_at=user.deleted_at,
    )


def user_dto_to_model(user: dtos.User) -> models.User:
    return models.User(
        id=user.id,
        username=user.username,
        hashed_password=user.hashed_password,
        deleted_at=user.deleted_at,
    )


def calendar_event_model_to_dto(calendar_event: models.CalendarEvent) -> dtos.CalendarEvent:
    return dtos.CalendarEvent(
        id=calendar_event.id,
        user_id=calendar_event.user_id,
        title=calendar_event.title,
        is_private=calendar_event.is_private,
        description=calendar_event.description,
        start_date=calendar_event.start_date,
        end_date=calendar_event.end_date,
    )


def calendar_event_dto_to_model(calendar_event: dtos.CalendarEvent) -> models.CalendarEvent:
    start_date = calendar_event.start_date
    if start_date:
        start_date = start_date.replace(tzinfo=None)

    end_date = calendar_event.end_date
    if end_date:
        end_date = end_date.replace(tzinfo=None)

    return models.CalendarEvent(
        id=calendar_event.id,
        user_id=calendar_event.user_id,
        title=calendar_event.title,
        is_private=calendar_event.is_private,
        description=calendar_event.description,
        start_date=start_date,
        end_date=end_date,
    )
