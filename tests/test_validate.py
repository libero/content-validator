import pytest
from validator.validate import validate_file, validate_relaxng, parse_file, parse_xml

TEST_DATA_PATH = 'tests/test_data/'
CONTENT_SCHEMA = 'tests/fixtures/schemas/api/content/data/content.rng'
FRONT_SCHEMA = 'tests/fixtures/schemas/api/content/data/parts/front.rng'


def validate_root(schema_file, xml_file):
    "validate a full file against a schema"
    return validate_file(schema_file, xml_file)


def validate_subelements(schema_file, xml_file, subelement=None):
    "validate subelements of an XML file against the schema"
    xml = parse_file(xml_file)
    schema = parse_file(schema_file)
    return validate_relaxng(schema, xml, subelement)


def test_validate_content_success():
    "full file against the content schema"
    schema_file = CONTENT_SCHEMA
    xml_file = TEST_DATA_PATH + 'content.xml'
    is_valid, messages = validate_root(schema_file, xml_file)
    assert is_valid is True
    assert messages == []


def test_validate_invalid_content_success():
    "invalid content file against the content schema will pass, all tags are allowed"
    schema_file = CONTENT_SCHEMA
    xml_file = TEST_DATA_PATH + 'content_invalid.xml'
    is_valid, messages = validate_root(schema_file, xml_file)
    assert is_valid is True
    assert messages == []


def test_validate_front_success():
    "full file against the front schema"
    schema_file = FRONT_SCHEMA
    xml_file = TEST_DATA_PATH + 'front.xml'
    is_valid, messages = validate_root(schema_file, xml_file)
    assert is_valid is True
    assert messages == []


def test_validate_content_parts_success():
    "content file parts against the front schema"
    schema_file = FRONT_SCHEMA
    xml_file = TEST_DATA_PATH + 'content.xml'
    is_valid, messages = validate_subelements(schema_file, xml_file, True)
    assert is_valid is True
    assert messages == []


def test_validate_invalid_content_parts_failure():
    "invalid content file parts against the front schema"
    schema_file = FRONT_SCHEMA
    xml_file = TEST_DATA_PATH + 'content_invalid.xml'
    is_valid, messages = validate_subelements(schema_file, xml_file, True)
    assert is_valid is False
    assert len(messages) == 7
    assert messages == [
        ('tests/test_data/content_invalid.xml:5:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMNAME: ' +
         'Expecting element front, got front_INVALID'),
        ('tests/test_data/content_invalid.xml:12:0:ERROR:RELAXNGV:RELAXNG_ERR_NOELEM: ' +
         'Expecting an element id, got nothing'),
        ('tests/test_data/content_invalid.xml:14:0:ERROR:RELAXNGV:RELAXNG_ERR_INTERSEQ: ' +
         'Invalid sequence in interleave'),
        ('tests/test_data/content_invalid.xml:14:0:ERROR:RELAXNGV:RELAXNG_ERR_CONTENTVALID: ' +
         'Element front failed to validate content'),
        ('tests/test_data/content_invalid.xml:19:0:ERROR:RELAXNGV:RELAXNG_ERR_NOELEM: ' +
         'Expecting an element title, got nothing'),
        ('tests/test_data/content_invalid.xml:22:0:ERROR:RELAXNGV:RELAXNG_ERR_INTERSEQ: ' +
         'Invalid sequence in interleave'),
        ('tests/test_data/content_invalid.xml:22:0:ERROR:RELAXNGV:RELAXNG_ERR_CONTENTVALID: ' +
         'Element front failed to validate content')
    ]


def test_validate_string_content_success():
    "string against the content schema"
    xml_string = u'<content xmlns="http://libero.pub"><tag></tag></content>'
    xml = parse_xml(xml_string)
    schema = parse_file(CONTENT_SCHEMA)
    is_valid, messages = validate_relaxng(schema, xml, None)
    assert is_valid is True
    assert messages == []


def test_validate_string_content_failure():
    "invalid string parts against the front schema will fail"
    xml_string = u'<content xmlns="http://libero.pub"><tag></tag></content>'
    xml = parse_xml(xml_string)
    schema = parse_file(FRONT_SCHEMA)
    is_valid, messages = validate_relaxng(schema, xml, True)
    assert is_valid is False
    assert len(messages) == 1
    assert messages == [
        '<string>:1:0:ERROR:RELAXNGV:RELAXNG_ERR_ELEMNAME: Expecting element front, got tag'
    ]
