from typing import Any, Mapping
from starlette.background import BackgroundTask

import pandas as pd

from loguru import logger

from fastapi.responses import Response, PlainTextResponse


class XMLRender(Response):
    """
    Рендер XML ответа
    """
    media_type = 'application/xml'
    charset = 'utf-8'

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self,
               value: Any,
               ) -> PlainTextResponse:
        logger.debug(f'get path xml {value}')
        xml = pd.read_xml(value,
                          iterparse={'product': ['id',
                                                 'name',
                                                 'quantity',
                                                 'price',
                                                 'category',
                                                 ],
                                     },
                          encoding=self.charset,
                          )
        return xml.to_xml().encode(self.charset)


def render(
    value: Any,
    accept: str | None,
    status_code: int | None,
    headers: dict[str, str] | None,
    renderers: list[Response] | None = None,
):
    """
    Рендерит ответ того типа,
    исходя из которого был запрос (Media Type)
    """
    renderers = renderers or [XMLRender]
    if accept:
        for media_type in accept.split(','):
            media_type = media_type.split(';')[0].strip()
            for renderer in renderers:
                if media_type in renderer.media_type:
                    initialization: Response = renderer(
                        content=value,
                        status_code=status_code,
                        headers=headers,
                        media_type=media_type,
                        )
                    logger.debug(f'in render path {value}')
                    return initialization
    renderer = renderers[0]
    media_type = renderer.media_types[0]
    initialization: Response = renderer(
        content=value,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
        )
    logger.debug(f'in render path {value}')
    return initialization
