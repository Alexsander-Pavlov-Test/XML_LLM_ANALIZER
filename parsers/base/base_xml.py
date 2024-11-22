from typing import Generator, TextIO, Any

from .abc import AbstractXMLParser
from . import BaseModelNotProvideError


class BaseXMLParser(AbstractXMLParser):
    """
    XML парсер
    """
    PARSER = None

    def __init__(self,
                 xml: str | TextIO,
                 target_items: str,
                 head_name: str | None = None,
                 ) -> None:
        self.xml = xml
        self._check_xml_instance(xml=xml)
        self.target_items = target_items
        self.head_name = head_name

    @classmethod
    def get_parser(cls):
        """
        Получение текущего парсера
        """
        parser = cls.PARSER
        if not parser:
            raise BaseModelNotProvideError(
                'Вы не можете использовать базовый класс',
                )
        return parser

    def _check_xml_instance(self, xml: str | TextIO) -> None:
        cls = type(self).__name__
        raise BaseModelNotProvideError(
                f'Вы не можете использовать базовый класс {cls}',
                )

    def _parse(self,
               xml,
               target_items,
               ) -> list[dict[str, str]] | None:
        """
        Метод парсинга данных из XML
        """
        parser = self.get_parser()

    def get_list(self) -> list[dict[str, str]] | None:
        """
        Возвращает список после парсинга
        """
    
    def get_generator(self) -> Generator[dict[str, str], Any] | None:
        """
        Возвращает генератор после парсинга
        """
