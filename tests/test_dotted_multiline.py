from __future__ import unicode_literals

import pytest

import toml


@pytest.mark.parametrize('delimiter', ["'''", '"""'])
@pytest.mark.parametrize('prefix', ['', '[section]\n'])
def test_multiline_dotted_key_keeps_its_parent_and_following_siblings(
        delimiter, prefix):
    source = (prefix + 'key.sub = ' + delimiter + '\nmultiline string\n' +
              delimiter + '\nsibling = 7\nkey.other = 8\n')
    expected = {'key': {'sub': 'multiline string\n', 'other': 8},
                'sibling': 7}
    if prefix:
        expected = {'section': expected}
    assert toml.loads(source) == expected


def test_multiline_dotted_keys_in_separate_array_elements():
    source = ('[[items]]\nmeta.description = """\nfirst\n"""\nid = 1\n'
              '[[items]]\nmeta.description = """\nsecond\n"""\nid = 2\n')
    assert toml.loads(source) == {'items': [
        {'meta': {'description': 'first\n'}, 'id': 1},
        {'meta': {'description': 'second\n'}, 'id': 2},
    ]}


@pytest.mark.parametrize('key,expected_key', [
    ('"inner.name"', 'inner.name'), ("'inner=name'", 'inner=name'),
    ('"space name"', 'space name'),
])
def test_quoted_leaf_does_not_lose_its_key_syntax(key, expected_key):
    source = 'outer.' + key + ' = """\ntext\n"""\n'
    assert toml.loads(source) == {'outer': {expected_key: 'text\n'}}


def test_dotted_array_of_multiline_strings_keeps_its_parent():
    source = 'outer.values = ["""first\nline""", """second\nline"""]\n'
    assert toml.loads(source) == {
        'outer': {'values': ['first\nline', 'second\nline']},
    }


def test_multiline_continuation_with_custom_dict():
    class CustomDict(dict):
        pass

    source = 'outer.inner.value = """one\\\n  two\n"""\nafter = 1\n'
    parsed = toml.loads(source, _dict=CustomDict)
    assert parsed == {'outer': {'inner': {'value': 'onetwo\n'}}, 'after': 1}
    assert isinstance(parsed['outer']['inner'], CustomDict)


def test_duplicate_multiline_dotted_key_is_rejected():
    with pytest.raises(toml.TomlDecodeError, match='Duplicate keys'):
        toml.loads('outer.value = "first"\nouter.value = """second\nline"""')
