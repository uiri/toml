import pytest

import toml


@pytest.mark.parametrize('quote', ['"""', "'''"])
@pytest.mark.parametrize('wrapper', ['value = { text = %s, count = 2 }',
                                     'value = { nested = { text = %s } }',
                                     'value = [{ text = %s }]'])
def test_multiline_string_in_inline_table(quote, wrapper):
    text = 'first line\n  second = line # literal\n}\nlast line\n'
    source = wrapper % (quote + '\n' + text + quote)
    parsed = toml.loads(source + '\nafter = true\n')
    value = parsed['value']
    if isinstance(value, list):
        value = value[0]
    if 'nested' in value:
        value = value['nested']
    assert value['text'] == text
    assert parsed['after'] is True
    assert toml.loads(toml.dumps(parsed)) == parsed


def test_poe_release_shell_in_inline_table():
    source = '''[tool.poe.tasks]
style = [
    { cmd = "black .", help = "Run black on the code base" },
    { cmd = "isort .", help = "Run isort on the code base" },
]
release = { shell = """
    set -e
    poetry version minor
    version=$(poetry version --short)
    git commit pyproject.toml -m "Bump version to ${version}"
    git tag ${version}
    git push && git push --tags
    poetry build && poetry publish
""" }
'''
    shell = source.split('"""', 2)[1][1:]
    result = toml.loads(source)
    assert result['tool']['poe']['tasks']['release']['shell'] == shell
    assert len(result['tool']['poe']['tasks']['style']) == 2


@pytest.mark.parametrize('source', [
    'value = { text = "first\nsecond" }',
    'value = { text = """first\nsecond""",\ncount = 2 }',
])
def test_only_multiline_string_values_may_span_inline_table_lines(source):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads(source)


def test_error_after_inline_multiline_string_keeps_source_position():
    source = 'value = { text = """first\nsecond""" }\nafter = ???\n'
    with pytest.raises(toml.TomlDecodeError) as caught:
        toml.loads(source)
    assert caught.value.lineno == 3
    assert caught.value.pos == source.index('after')
