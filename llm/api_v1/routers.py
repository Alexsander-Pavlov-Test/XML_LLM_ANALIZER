from fastapi import FastAPI

from config import settings
from api_v1.api_analyst.views import router as analyst


def register_routers(app: FastAPI) -> None:
    """
    Функция по регистрации роутеров
    """
    app.include_router(
        router=analyst,
        prefix=settings.API_PREFIX,
        )
