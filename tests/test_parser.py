import pytest
from parsers import FileXMLParser, StringXMLParser


class TestParser:
    """
    Тесты парсера
    """
    
    @pytest.mark.parser
    def test_leng_xml_parse(self, file_xml):
        print(file_xml)
        parser = StringXMLParser(file_xml, 'product')
        assert len(parser.get_list()) == 1
