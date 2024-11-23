import operator
from typing import TextIO
from collections.abc import Sequence, Generator, Callable
from collections import defaultdict
from xml.dom.minicompat import NodeList
from xml.dom.minidom import Document, Element
from xml.parsers.expat import ExpatError

from parsers.base_parser.abc import AbstractXMLParser
from parsers.base_parser.exeptions import (
    BaseModelNotProvideError,
    XMLParseError,
    )
from parsers.base_parser.parse_except import parse_expat_error
from parsers.base_converter import BaseTypeConverter
from parsers.type_converters import DefaultTypeConverter


class BaseXMLParser(AbstractXMLParser):
    """
    Базовый XML парсер
    """
    PARSER = None

    def __init__(self,
                 xml: str | TextIO,
                 target_items: str,
                 attrs: Sequence[str] | None = None,
                 type_converter: BaseTypeConverter | None = DefaultTypeConverter,
                 convert_int: bool = True,
                 convert_float: bool = True,
                 convert_date: bool = True,
                 ) -> None:
        self.xml = xml
        self._check_xml_instance(xml=xml)
        self.target_items = target_items
        self.values = tuple(attrs) if attrs else attrs
        self._attrs: dict[str, str] | None = None
        self._type_converter = type_converter
        self.convert_int = bool(convert_int)
        self.convert_float = bool(convert_float)
        self.convert_date = bool(convert_date)
        self.items = self._parse(
            xml=xml,
            target_items=target_items,
            attrs=attrs,
            type_converter=type_converter,
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
        return

    def _check_xml_instance(self, xml: str | TextIO) -> None:
        cls = type(self).__name__
        raise BaseModelNotProvideError(
                f'Вы не можете использовать базовый класс {cls}',
                )

    def _stuct_list_items(self,
                          list_elements: NodeList[Element],
                          type_converter: BaseTypeConverter | None,
                          ) -> Generator[dict[str, str], None, None]:
        """
        Вывод списка items
        """
        for element in list_elements:
            parsed_dict = dict()
            for item in element.childNodes:
                if item.firstChild:
                    parsed_dict[item.nodeName] = item.firstChild.nodeValue
            if type_converter:
                converter = type_converter(
                    parsed_dict,
                    self.convert_int,
                    self.convert_float,
                    self.convert_date,
                )
                yield converter.convert()
            else:
                yield parsed_dict

    def _get_attrs(self,
                   document: Document,
                   attrs: Sequence[str],
                   type_converter: DefaultTypeConverter | None,
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
        if type_converter:
            converter = type_converter(
                result,
                self.convert_int,
                self.convert_float,
                self.convert_date,
            )
            self._attrs = converter.convert()
        else:
            self._attrs = result

    def _get_items_target(self,
                          document: Document,
                          target_items: str,
                          ) -> NodeList[Element]:
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
               type_converter: BaseTypeConverter | None,
               ) -> Generator[dict[str, str], None, None] | list[None]:
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
                type_converter=type_converter,
            )
        list_elements = self._get_items_target(
            document=document,
            target_items=target_items,
        )
        if list_elements:
            list_parse_items = self._stuct_list_items(
                list_elements=list_elements,
                type_converter=type_converter,
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
        return list(self.items)

    def get_generator(self) -> (Generator[dict[str, str],None, None] |
                                list[None]):
        """
        Возвращает генератор после парсинга
        """
        return self.items