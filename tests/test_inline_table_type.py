from collections import OrderedDict

import pytest
import toml
from toml.decoder import InlineTableDict


@pytest.mark.parametrize('dict_type', [dict, OrderedDict])
def test_inline_tables_share_a_type_within_a_decoder(dict_type):
    decoder = toml.TomlDecoder(_dict=dict_type)
    data = toml.loads('a = {x = 1}\nb = {y = 2, nested = {z = 3}}',
                      decoder=decoder)
    assert type(data['a']) is type(data['b'])
    assert type(data['a']) is type(data['b']['nested'])
    assert isinstance(data['a'], dict_type)
    assert isinstance(data['a'], InlineTableDict)
    assert data['a'] is not data['b']
    data['a']['x'] = 9
    assert data['b'] == {'y': 2, 'nested': {'z': 3}}
    assert type(decoder.get_empty_inline_table()) is type(data['a'])


def test_inline_table_factory_preserves_custom_mapping():
    class CustomDict(dict):
        pass

    decoder = toml.TomlDecoder(_dict=CustomDict)
    first = decoder.get_empty_inline_table()
    second = decoder.get_empty_inline_table()
    assert type(first) is type(second)
    assert isinstance(first, CustomDict)
    default_table = toml.TomlDecoder().get_empty_inline_table()
    assert not isinstance(first, type(default_table))
