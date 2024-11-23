import operator
from typing import TextIO
from collections.abc import Sequence, Generator, Callable
from collections import defaultdict
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element
from xml.parsers.expat import ExpatError

from parsers.base.abc import AbstractXMLParser
from parsers.base.exeptions import (
    BaseModelNotProvideError,
    XMLParseError,
    HeadNotFoundError,
    )
from parsers.base.parse_except import parse_expat_error


class BaseXMLParser(AbstractXMLParser):
    """
    Базовый XML парсер
    """
    PARSER = None

    def __init__(self,
                 xml: str | TextIO,
                 target_items: str,
                 attrs: Sequence[str] | None = None,
                 ) -> None:
        self.xml = xml
        self._check_xml_instance(xml=xml)
        self.target_items = target_items
        self.values = tuple(attrs)
        self._attrs: dict[str, str] | None = None
        self.items = self._parse(
            xml=xml,
            target_items=target_items,
            attrs=attrs,
            )

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
                          list_elements: Generator[NodeList[Element], None, None],
                          ):
        """
        Вывод списка items
        """
        list_parse_items = [{item.nodeName: item.firstChild.nodeValue
                             for item
                             in element.childNodes
                             if item.firstChild}
                            for element
                            in list_elements]
        return list_parse_items

    def _get_attrs(self,
                   document: Document,
                   attrs: Sequence[str],
                   ) -> None:
        result = defaultdict(str)
        for attr in attrs:
            result[attr]
            curr_nodes = document.childNodes
            while curr_nodes:
                for node in curr_nodes:
                    if attr in node.attributes:
                        result.update({attr: node.attributes.get(attr).nodeValue})
                curr_nodes = [node for node in curr_nodes[0].childNodes if node.firstChild]
        self._attrs = result

    def _get_items_target(self,
                          document: Document,
                          target_items: str,
                          ) -> Generator[NodeList[Element], None, None]:
        items = document.getElementsByTagName(target_items)
        return items

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
               attrs: Sequence[str] | None,
               ) -> list[dict[str, str]] | list[None]:
        """
        Метод парсинга данных из XML
        """
        parser = self.get_parser()
        document = self._get_document(
            xml=xml,
            parser=parser,
        )
        if attrs:
            self._get_attrs(
                document=document,
                attrs=attrs,
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

    @property
    def attrs(self) -> dict[str, str]:
        return self._attrs

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
