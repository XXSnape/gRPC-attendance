from core.config import settings
from fastapi import APIRouter

from .lessons import router as lessons_router
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
    responses={401: {"description": "Не авторизован"}},
)

router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(
    lessons_router,
    prefix=settings.api.v1.lessons,
)
