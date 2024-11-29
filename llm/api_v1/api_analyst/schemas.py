from pydantic import BaseModel


class GetDataAnalystSchema(BaseModel):
    """
    Схема получения данных для аналитика
    """
    text: str


class ResponseAnalystSchema(BaseModel):
    """
    Схема ответа аналитика
    """
    generated_text: str
