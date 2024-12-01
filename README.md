# LLM Анализатор для XML файлов на основе выборки
Данный проект реализует множество различных функциональностей.
## Цель
Цель проекта это парсинг XML документа из определенного энд поинта
по определенному периоду времени, затем составление Prompt для LLM модели,
после всех действий данные отдаются LLM модели которая в свою очередь 
анализирует данные и отдает ответ - ответ сохраняется в Базу Данных.
## Структура
В Проекте Реализованна микросервесная архитектура
Микросервисы:
 - analizer
 - xml
 - llm
### analizer
Сервис analizer отвечает за обработку XML файлов, а так же
является центральным сервисом который занимается переодическими 
задачами по обработке всех данных и запросов в другие сервисы.
### Реализованные классы
- Парсеры
    Парсеры неоходимы для парсинга неформальных данных
    и перепределяют данные в необходимую структуру.
    - BaseXMLParser
    - StringXMLParser
    - FileXMLParser

    BaseXMLParser
    Базовый класс XML парсера, предназначен только для 
    наследование и реализует базовую функциональность.

    StringXMLParser
    Парсер который специализируется на парсинге строковой модели данных
    ```python
    from config import settings
    from parsers import StringXMLParser

    # response ответ от Энд Поинта
    body = response.content.decode(encoding='utf-8')
    parser = StringXMLParser(xml=body,
                             target_items=settings.TARGET_ITEMS_XML,
                             attrs=(settings.TARGET_ATTRS_XML,),
                             )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```

    FileXMLParser
    Парсер который специализируется на парсинге Файла
    ```python
    from config import settings
    from pathlib import Path
    from parsers import FileXMLParser


    path = Path('some_xml_file')

    # Открытие файла
    with path.open(mode='r', encoding='utf-8') as file_:
        parser = FileXMLParser(xml=file_,
                               target_items=settings.TARGET_ITEMS_XML,
                               attrs=(settings.TARGET_ATTRS_XML,),
                               )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```
- Конверторы типов
    Конверторые типов играют важную роль в фазе парсинга,
    они обеспечивают нужный тип данных для дальнейшей обработке
    на протяжении всего парсинга.
    - BaseTypeConverter
    - DefaultTypeConverter

    BaseTypeConverter
    Базовый конвертор предназначен только для наследования,
    реализует базовый функционал.

    DefaultTypeConverter
    "Дэфолтный" конвертор который стандартным образом
    обеспечивает конвертацию данных.

    ```python
    from config import settings
    from parsers import StringXMLParser
    from parsers.type_converters import DefaultTypeConverter

    # response ответ от Энд Поинта
    body = response.content.decode(encoding='utf-8')
    parser = StringXMLParser(xml=body,
                             target_items=settings.TARGET_ITEMS_XML,
                             attrs=(settings.TARGET_ATTRS_XML,),
                             type_converter=DefaultTypeConverter,
                             convert_int=True,
                             convert_float=True,
                             convert_date=True,
                             )
    # Получение генератора
    parsed_items = parser.get_generator()
    ```
- Создатель Промпров
    Этот важный класс отвечает за правильную и надежную
    генерацию запроса для LLM.
    - ProductPromptMaker

    ProductPromptMaker
    Генерирует Промпт для LLM модели

    ```python
    from datetime import date
    from task_schedule.utils import ProductPromptMaker


    date = date(2024, 1, 1)
    session = AsyncSession
    prompt_maker = ProductPromptMaker(
        session=session,
        date=date
    )
    prompt = await prompt_maker.get_prompt()
    ```
### xml
