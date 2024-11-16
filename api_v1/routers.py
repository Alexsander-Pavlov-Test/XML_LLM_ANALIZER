from fastapi import APIRouter
from api_v1.products.views import router as products


router = APIRouter(prefix='/api/v1')
router.include_router(products)
