from collections.abc import Sequence
from abc import ABC, abstractmethod
from typing import ClassVar
from xml.dom.minidom import parse, parseString


class AbstractXMLParser(ABC, Sequence):
    """
    Абстрактный класс XML Парсера
    """
    PARSER: ClassVar['parse' | 'parseString' | None] = None

    @abstractmethod
    @classmethod
    def get_parser(cls):
        pass
