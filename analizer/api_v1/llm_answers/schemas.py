from pydantic import BaseModel
from datetime import date


class AnswerSchema(BaseModel):
    """
    Схема ответа от LLM модели
    """
    id: int
    date: date
    answer: str
