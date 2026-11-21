from collections import defaultdict
from functools import partial

import pytest

import toml


class DefaultTable(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DefaultTable, self).__init__(dict, *args, **kwargs)


@pytest.mark.parametrize('factory', [DefaultTable, partial(defaultdict, dict)])
@pytest.mark.parametrize('document', [
    'value = 1',
    '[section]\nvalue = 1',
    '[parent.child]\nvalue = 1\n[parent]\nname = "parent"',
    'parent.child.value = 1',
    '[[items]]\nvalue = 1\n[[items]]\nvalue = 2',
    '[[items]]\n[items.config]\nvalue = 1\n'
    '[[items]]\n[items.config]\nvalue = 2',
])
def test_defaultdict_tables(factory, document):
    result = toml.loads(document, _dict=factory)
    assert result == toml.loads(document)
    assert isinstance(result, defaultdict)
    assert result.default_factory is dict
    result['missing']['new'] = 3
    assert result['missing'] == {'new': 3}


@pytest.mark.parametrize('document', [
    'value = 1\nvalue = 2',
    '[section]\nvalue = 1\nvalue = 2',
    '[section]\nvalue = 1\n[section]\nother = 2',
])
def test_defaultdict_duplicate_definitions(document):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads(document, _dict=DefaultTable)
