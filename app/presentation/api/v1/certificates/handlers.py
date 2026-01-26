from fastapi import APIRouter

from presentation.api.v1.certificates.certificate_groups_handlers import router as certificate_groups_router
from presentation.api.v1.certificates.certificates_handlers import router as certificates_router


router = APIRouter()
router.include_router(certificate_groups_router)
router.include_router(certificates_router)
