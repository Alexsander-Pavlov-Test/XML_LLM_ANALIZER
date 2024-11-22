from fastapi import FastAPI

from config import settings
from api_v1.products.views import router as products


def register_routers(app: FastAPI) -> None:
    """
    Функция по регистрации роутеров
    """
    app.include_router(
        router=products,
        prefix=settings.API_PREFIX,
        )
