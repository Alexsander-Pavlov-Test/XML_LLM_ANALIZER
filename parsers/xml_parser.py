import pathlib
import os
from typing import TextIO
from xml.dom.minidom import parse, parseString

from parsers.base_parser import BaseXMLParser
from parsers.base_parser.exeptions import XMLParseError
from api_v1.regex import check_xml_file


class StringXMLParser(BaseXMLParser):
    """
    XML парсер строчного типа
    """
    PARSER = parseString

    def _check_xml_instance(self, xml: str) -> None:
        if not isinstance(xml, str):
            cls = type(self).__name__
            raise XMLParseError('Ошибка: Не возможно обработать '
                                f'{xml} с помощью {cls} '
                                f'попробуйте {FileXMLParser.__name__}')

        if not xml.startswith('<?'):
            raise XMLParseError('Ошибка: XML файл должен иметь заголовок по '
                                'типу <?xml version="1.0" encoding="utf-8"?>')


class FileXMLParser(BaseXMLParser):
    """
    XML парсер файлового типа

    (str): Путь к файлу

    (TextIO): Объект файла
    """
    PARSER = parse

    def _is_file(self, xml: str | TextIO) -> bool:
        if isinstance(xml, os.PathLike | str):
            self.xml = str(xml)
            path = pathlib.Path(xml)
            if path.is_file:
                is_xml = check_xml_file(path.name)
                if not is_xml:
                    raise XMLParseError(f'Ошибка: Файл {path.name} не XML '
                                        f'попробуйте {StringXMLParser.__name__}')
                if not path.exists():
                    raise XMLParseError(
                        f'Ошибка: Файл по пути {path.as_posix()} не найден',
                        )
            else:
                raise XMLParseError(f'Ошибка: {path.as_posix()} не файл')
        else:
            xml_name = pathlib.Path(xml.name)
            is_xml = check_xml_file(xml_name.name)
            if not is_xml:
                raise XMLParseError(f'Ошибка: не верный формат файла {xml_name.name}')
            first_char = xml.read(1)
            if not first_char:
                raise XMLParseError(f'Ошибка: файл пустой')
            xml.seek(0)

    def _check_xml_instance(self, xml: str | TextIO) -> None:
        self._is_file(xml=xml)
