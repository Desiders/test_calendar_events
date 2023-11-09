import logging

from fastapi import APIRouter

from .auth import router as auth_router
from .calendar_events import router as calendar_events_router
from .main import router as main_router

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["public", "html"],
)

router.include_router(main_router)
router.include_router(auth_router)
router.include_router(calendar_events_router)
