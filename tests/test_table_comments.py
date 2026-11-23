from collections import OrderedDict

import pytest

import toml


def roundtrip(source, table_type=dict):
    decoder = toml.TomlPreserveCommentDecoder(table_type)
    encoder = toml.TomlPreserveCommentEncoder(table_type)
    parsed = toml.loads(source, decoder=decoder)
    output = toml.dumps(parsed, encoder=encoder)
    assert toml.loads(output) == toml.loads(source)
    return parsed, output


@pytest.mark.parametrize('header', ['[section]', '[[section]]'])
@pytest.mark.parametrize('comment', [' # inline\n', '\n# first comment\n'])
def test_comment_after_table_header(header, comment):
    source = header + comment + 'value = "kept"\n'
    _, output = roundtrip(source)
    assert output.index('#') > output.index(header)
    assert output.index('#') < output.index('value =')
    assert comment.strip() in output


def test_comments_stay_with_their_table():
    source = ('[first]\nvalue = 1 # first value\n'
              '[second] # second header\n# second table\nvalue = 2\n')
    _, output = roundtrip(source)
    first, second = output.split('[second]')
    assert '# first value' in first
    assert '# second header' not in first
    assert '# second table' not in first
    assert '# second header' in second
    assert '# second table' in second


def test_each_array_table_keeps_its_comments():
    source = ('[[products]]\n# Nail\nname = "Nail"\n'
              '[[products]] # Hammer\nname = "Hammer"\n')
    _, output = roundtrip(source)
    _, first, second = output.split('[[products]]')
    assert '# Nail' in first and '# Hammer' not in first
    assert '# Hammer' in second and '# Nail' not in second


@pytest.mark.parametrize('source', [
    '[empty] # kept',
    '[empty]\n# kept',
    '[empty]\n# kept\n',
    '# kept',
    'value = 1 # kept',
])
def test_comments_at_end_of_input(source):
    _, output = roundtrip(source)
    assert output.count('# kept') == 1


def test_parent_comment_survives_when_it_only_contains_tables():
    source = '[parent]\n# parent comment\n[parent.child]\nvalue = 1\n'
    _, output = roundtrip(source)
    assert output.index('[parent]') < output.index('# parent comment')
    assert output.index('# parent comment') < output.index('[parent.child]')


def test_leading_comments_and_custom_dictionary():
    source = '# document comment\n[section]\n# section comment\nvalue = 1\n'
    parsed, output = roundtrip(source, OrderedDict)
    assert isinstance(parsed, OrderedDict)
    assert isinstance(parsed['section'], OrderedDict)
    assert output.startswith('# document comment\n')
    assert '# section comment' in output.split('[section]')[1]
