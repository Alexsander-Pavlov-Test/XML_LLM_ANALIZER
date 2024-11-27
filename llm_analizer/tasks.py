import httpx

from api_v1.products.dao import ProductDAO
from parsers import StringXMLParser
from parsers.base_parser.exeptions import NoDataParseError
from llm_analizer.utils import union_each_one_data
from llm_analizer.utils import ProductPromptMaker
from config import (
    celery_app,
    settings,
    db_connection,
    )


@celery_app.task
async def get_analize_products_endpoint_task():
    """
    Задача по получении сущностей из энд поинта.

    Сущности являются (XML) структурой которые в последствии
    парсятся в Dictiontary модель данных с конвертацие типов.

    Затем сущности сохраняются в базу данных.
    
    Отдельный класс генерирует промпр для LLM, исходя из указанной даты,
    делает все необходимые аналитические выборки из базы данных.

    После всех действий данные отдаются LLM модели,
    которая в свою очередь анализирует данные по промпру
    и выводит результат.

    Результат сохраняется в отдельную таблицу в базе данных,
    и может помочь при дальнейшем анализе.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url=settings.TASK_END_POINT_URL)
    body = response.content.decode(encoding='utf-8')
    parser = StringXMLParser(xml=body,
                             target_items=settings.TARGET_ITEMS_XML,
                             attrs=(settings.TARGET_ATTRS_XML,),
                             )
    parsed_items = parser.get_generator()
    attrs = parser.attrs
    date = attrs.get('date')
    values_to_save = union_each_one_data(
        data=attrs,
        data_to_each=parsed_items,
    )

    if not parsed_items:
        raise NoDataParseError('Нет данных для обработки')
    async with db_connection.session() as session:
        await ProductDAO.add_multiple(
            session=session,
            list_values=values_to_save,
        )
        prompt_maker = ProductPromptMaker(
            session=session,
            date=date
        )
        prompt = await prompt_maker.get_prompt()


celery_app.conf.beat_schedule = {
    'task-every-day-analizer': {
        'task': 'llm_analizer.tasks.get_analize_products_endpoint_task',
        'schedule': settings.celery.TIMEDELTA_PER_DAY,
    },
}
