from fastapi import APIRouter

from presentation.api.v1.auth.handlers import router as auth_router
from presentation.api.v1.certificates.handlers import router as certificates_router
from presentation.api.v1.media.handlers import router as media_router
from presentation.api.v1.news.handlers import router as news_router
from presentation.api.v1.portfolios.handlers import router as portfolios_router
from presentation.api.v1.products.handlers import router as products_router
from presentation.api.v1.seo_settings.handlers import router as seo_settings_router
from presentation.api.v1.submissions.handlers import router as submissions_router
from presentation.api.v1.users.handlers import router as users_router
from presentation.api.v1.vacancies.handlers import router as vacancies_router


v1_router = APIRouter()

v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(media_router)
v1_router.include_router(news_router)
v1_router.include_router(vacancies_router)
v1_router.include_router(submissions_router)
v1_router.include_router(portfolios_router)
v1_router.include_router(products_router)
v1_router.include_router(seo_settings_router)
v1_router.include_router(certificates_router)
