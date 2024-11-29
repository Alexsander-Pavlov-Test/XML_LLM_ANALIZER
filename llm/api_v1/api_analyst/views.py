from fastapi import APIRouter

from llm_analizer import Qwen
from .schemas import ResponseAnalystSchema, GetDataAnalystSchema


router = APIRouter(prefix='/llm',
                   tags=['LLM'],
                   )


@router.put(path='/analyst-manager',
            description='Send Prompt to Analyst',
            name='Request to Analyst',
            )
async def request_analys(text: GetDataAnalystSchema) -> list[ResponseAnalystSchema]:
    analyst = Qwen
    response = analyst.make_question(text.text)
    return response
