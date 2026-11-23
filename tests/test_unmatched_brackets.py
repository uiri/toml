import pytest

import toml


@pytest.mark.parametrize('prefix', [
    'list_1 = [{name=1}]',
    'value = []',
    'value = [1, 2]',
    'value = [[1], [2]]',
    'value = [\n  1,\n  2,\n]',
    '[section]',
    '[[section]]',
    'value = ["]"] ',
])
def test_extra_closing_bracket_is_rejected_at_its_source_position(prefix):
    document = prefix + ']\nlist_2 = [{name=2}]\n'
    with pytest.raises(toml.TomlDecodeError) as error:
        toml.loads(document)
    assert error.value.pos == len(prefix)
    assert 'closing bracket' in str(error.value)


@pytest.mark.parametrize('document, expected', [
    ('list_1 = [{name=1}]\nlist_2 = [{name=2}]',
     {'list_1': [{'name': 1}], 'list_2': [{'name': 2}]}),
    ('value = [[1], [2]]', {'value': [[1], [2]]}),
    ('value = [\n 1, # ignored ]\n 2,\n]', {'value': [1, 2]}),
    ('value = ["]", "x[y"]', {'value': [']', 'x[y']}),
    ("value = '[]'", {'value': '[]'}),
    ('value = """first ]\nsecond ["""', {'value': 'first ]\nsecond ['}),
    ('"key]" = []\n# ignored ]', {'key]': []}),
    ('[section]\nvalue = []\n[[items]]\nvalue = [1]',
     {'section': {'value': []}, 'items': [{'value': [1]}]}),
])
def test_balanced_and_non_delimiter_brackets_still_parse(document, expected):
    assert toml.loads(document) == expected
