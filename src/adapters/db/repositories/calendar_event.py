from uuid import UUID

from sqlalchemy import delete, select

from src.adapters.db.converters import calendar_event_dto_to_model, calendar_event_model_to_dto
from src.adapters.db.models import CalendarEvent
from src.dtos import CalendarEvent as CalendarEventDTO
from src.exceptions import CalendarEventIDNotFound

from .base import SQLAlchemyRepo


class CalendarEventRepo(SQLAlchemyRepo):
    async def get_by_id(self, id: UUID) -> CalendarEventDTO:
        calendar_event = await self._session.scalar(select(CalendarEvent).filter(CalendarEvent.id == id))

        if calendar_event is None:
            raise CalendarEventIDNotFound(id)

        return calendar_event_model_to_dto(calendar_event)

    async def get_by_user_id(self, user_id: UUID) -> list[CalendarEventDTO]:
        calendar_events = await self._session.scalars(select(CalendarEvent).filter(CalendarEvent.user_id == user_id))

        return [calendar_event_model_to_dto(calendar_event) for calendar_event in calendar_events]

    async def delete_by_id(self, id: UUID) -> None:
        await self._session.execute(delete(CalendarEvent).filter(CalendarEvent.id == id))

    async def add(self, calendar_event: CalendarEventDTO) -> None:
        self._session.add(calendar_event_dto_to_model(calendar_event))

        await self._session.flush()

    async def update(self, calendar_event: CalendarEventDTO) -> None:
        await self._session.merge(calendar_event_dto_to_model(calendar_event))
