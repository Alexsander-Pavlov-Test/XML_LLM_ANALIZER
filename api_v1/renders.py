from typing import Any, ClassVar
from abc import ABC, abstractmethod


class Renderer(ABC):
    """
    Абстрактный каркасный класс Рендера
    """
    media_types: ClassVar[tuple[str, ...]] = None

    @abstractmethod
    def render(self,
               value: Any,
               status_code: int = 200,
               headers: dict[str, str] | None = None,
               media_type: str | None = None,
               ):
        """
        Метод рендера
        """

        pass


def render(
    value: Any,
    accept: str | None,
    status_code: int | None,
    headers: dict[str, str] | None,
    renderers: list[Renderer] | None = None,
):
    """
    Рендерит ответ того типа,
    исходя из которого был запрос (Media Type)
    """
    renderers = renderers or []
    if accept:
        for media_type in accept.split(','):
            media_type = media_type.split(';')[0].strip()
            for renderer in renderers:
                if media_type in renderer.media_types:
                    initialization: Renderer = renderer()
                    return initialization.render(
                        value=value,
                        status_code=status_code,
                        headers=headers,
                        media_type=media_type,
                    )
    renderer = renderers[0]
    media_type = renderer.media_types[0]
    return renderer.render(
        value=value,
        status_code=status_code,
        headers=headers,
        media_type=media_type,
    )
