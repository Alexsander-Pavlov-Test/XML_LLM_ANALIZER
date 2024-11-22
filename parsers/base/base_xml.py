import operator
from typing import Generator, TextIO, Callable
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element
from xml.parsers.expat import ExpatError

from parsers.base.abc import AbstractXMLParser
from parsers.base.exeptions import BaseModelNotProvideError, XMLParseError
from parsers.base.parse_except import parse_expat_error


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
        self.items = self._parse(xml=xml, target_items=target_items)

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

    def __getitem__(self, index):
        index = operator.index(index)
        return self.items[index]

    def __len__(self) -> int:
        return len(self.items)

    def _check_xml_instance(self, xml: str | TextIO) -> None:
        cls = type(self).__name__
        raise BaseModelNotProvideError(
                f'Вы не можете использовать базовый класс {cls}',
                )

    def _stuct_list_items(self,
                          list_elements: Generator[NodeList[Element]],
                          ):
        """
        Вывод списка items
        """
        list_parse_items = [{item.nodeName: item.firstChild
                             for item
                             in element.childNodes
                             if item.firstChild}
                            for element
                            in list_elements]
        return list_parse_items

    def _get_items_target(self,
                          document: Document,
                          target_items: str,
                          ) -> Generator[NodeList[Element], None, None]:
        items = document.getElementsByTagName(target_items)
        yield items

    def _get_document(self,
                      xml: str | TextIO,
                      parser: Callable[[str | TextIO], Document],
                      ) -> Document:
        try:
            document = parser(xml)
        except ExpatError as ex:
            msg = parse_expat_error(ex=ex)
            raise XMLParseError(msg)
        return document

    def _parse(self,
               xml: str | TextIO,
               target_items: str,
               ) -> list[dict[str, str]] | list[None]:
        """
        Метод парсинга данных из XML
        """
        parser = self.get_parser()
        document = self._get_document(
            xml=xml,
            parser=parser,
        )
        list_elements = self._get_items_target(
            document=document,
            target_items=target_items,
        )
        if list_elements:
            list_parse_items = self._stuct_list_items(
                list_elements=list_elements,
            )
            return list_parse_items
        return []

    def get_list(self) -> list[dict[str, str] | None]:
        """
        Возвращает список после парсинга
        """
        return self.items

    def get_generator(self) -> (Generator[dict[str, str],None, None] |
                                list[None]):
        """
        Возвращает генератор после парсинга
        """
        if self.items:
            for item in self.items:
                yield item
        return []
