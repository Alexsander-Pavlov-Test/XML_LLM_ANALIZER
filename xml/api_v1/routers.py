from fastapi import FastAPI

from config import settings
from api_v1.api_xml.views import router as xml


def register_routers(app: FastAPI) -> None:
    """
    Функция по регистрации роутеров
    """
    app.include_router(
        router=xml,
        prefix=settings.API_PREFIX,
        )
