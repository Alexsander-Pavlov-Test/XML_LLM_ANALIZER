from .abc import AbstractXMLParser
from . import BaseModelNotProvideError


class BaseXMLParser(AbstractXMLParser):
    """
    XML парсер
    """
    PARSER = None

    def __init__(self,
                 xml_string: str,
                 target_items: str,
                 head_name: str | None = None,
                 ) -> None:
        pass

    @classmethod
    def get_parser(cls):
        parser = cls.PARSER
        if not parser:
            raise BaseModelNotProvideError(
                'Вы не можете использовать базовый класс')
        return parser
