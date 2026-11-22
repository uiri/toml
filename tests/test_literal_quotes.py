import pytest

import toml


@pytest.mark.parametrize('text', [
    "['][\"]", "single ' quote", "two '' quotes", 'a "double" quote',
    "path\\'segment", "first ' line\nnext \" line", "quote '# not a comment",
])
def test_quotes_inside_multiline_literal_string(text):
    document = "value = '''" + text + "'''\nafter = 42\n"
    assert toml.loads(document) == {'value': text, 'after': 42}


def test_unterminated_multiline_literal_is_rejected():
    with pytest.raises(toml.TomlDecodeError):
        toml.loads("value = '''one ' quote\nafter = 42")
