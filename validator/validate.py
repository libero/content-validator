from io import StringIO
import lxml.etree as etree


def parse_xml(string):
    "convert string to file-like then parse as a file"
    return parse_file(StringIO(string))


def parse_file(xml_file):
    "most compatible is to parse from file"
    return etree.parse(xml_file)


def validate_file(schema_file, xml_file, element_name=None):
    schema = parse_file(schema_file)
    xml = parse_file(xml_file)
    return validate_relaxng(schema, xml, element_name)


def validate_relaxng(schema, xml, subelement=False):
    "validate the xml against the schema"
    is_all_valid = True
    error_messages = []
    relaxng = etree.RelaxNG(schema)
    # validate
    xml_list = []
    if subelement:
        # validate each of the sub elements
        for elem in xml.getroot():
            # create a new etree with the sub element as its root
            new_etree = etree.ElementTree(elem)
            xml_list.append(new_etree)
    else:
        xml_list.append(xml)
    for xml_element in xml_list:
        is_valid = relaxng.validate(xml_element)
        if not is_valid:
            # if any part is invalid then all is not valid
            is_all_valid = False
            error_messages += [str(error) for error in relaxng.error_log]
    return is_all_valid, error_messages
