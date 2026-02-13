from __future__ import annotations


def read_xml(xml_path: str):
    from lxml import etree

    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(xml_path, parser)
    return tree.getroot()


def extract_xpath_value(root, xpath: str) -> str | None:
    from lxml import etree

    result = root.xpath(xpath)
    if not result:
        return None
    first = result[0]
    if isinstance(first, etree._Element):
        return first.text
    return str(first)
