from fastapi import APIRouter

from presentation.api.v1.auth.handlers import router as auth_router
from presentation.api.v1.media.handlers import router as media_router
from presentation.api.v1.news.handlers import router as news_router
from presentation.api.v1.users.handlers import router as users_router
from presentation.api.v1.vacancies.handlers import router as vacancies_router


v1_router = APIRouter()

v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(media_router)
v1_router.include_router(news_router)
v1_router.include_router(vacancies_router)
