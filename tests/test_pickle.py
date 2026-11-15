from collections import OrderedDict
import copy
import pickle

import pytest
import toml
from toml.decoder import InlineTableDict


@pytest.mark.parametrize('protocol', range(pickle.HIGHEST_PROTOCOL + 1))
@pytest.mark.parametrize('dict_type', [dict, OrderedDict])
def test_pickle_inline_tables(protocol, dict_type):
    original = toml.loads(
        'table = { number = 1, nested = { enabled = true } }',
        _dict=dict_type)
    restored = pickle.loads(pickle.dumps(original, protocol=protocol))

    assert restored == original
    assert isinstance(restored, dict_type)
    assert isinstance(restored['table'], dict_type)
    assert isinstance(restored['table'], InlineTableDict)
    assert isinstance(restored['table']['nested'], InlineTableDict)
    encoder = toml.TomlPreserveInlineDictEncoder(_dict=dict_type)
    assert toml.dumps(restored, encoder=encoder) == toml.dumps(
        original, encoder=encoder)


@pytest.mark.parametrize('protocol', range(pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_inline_table_preserves_references(protocol):
    table = toml.loads('table = { number = 1 }')['table']
    table.description = 'inline table metadata'
    table['self'] = table
    restored = pickle.loads(pickle.dumps([table, table], protocol=protocol))
    assert restored[0] is restored[1]
    assert restored[0]['self'] is restored[0]
    assert restored[0]['number'] == 1
    assert restored[0].description == 'inline table metadata'


def test_copy_inline_table_preserves_marker():
    table = toml.loads('table = { number = 1 }')['table']
    for operation in (copy.copy, copy.deepcopy):
        restored = operation(table)
        assert restored == table
        assert restored is not table
        assert isinstance(restored, InlineTableDict)
