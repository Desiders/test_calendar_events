from fastapi import APIRouter

from .auth import router as auth_router
from .calendar_events import router as calendar_events_router
from .users import router as users_router

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(calendar_events_router)
