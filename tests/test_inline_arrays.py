import pytest

import toml


@pytest.mark.parametrize("value, expected", [
    ("[[], []]", [[], []]),
    ("[[1, 2], [3, 4]]", [[1, 2], [3, 4]]),
    ("[[[1], [2]], [[3], [4]]]", [[[1], [2]], [[3], [4]]]),
    ('[["a,b"], ["c,d"]]', [["a,b"], ["c,d"]]),
    ('[["[", "]", "{", "}"]]', [["[", "]", "{", "}"]]),
    ('[["a\\\",b"], ["c"]]', [['a",b'], ["c"]]),
    ('[["a\\\\"], ["b"]]', [["a\\"], ["b"]]),
    ("[['a\\b,c'], ['d']]", [["a\\b,c"], ["d"]]),
    ('[["""a, [b]"""], ["c"]]', [["a, [b]"], ["c"]]),
    ('[{x = [[], []]}, {x = [[1], [2]]}]',
     [{"x": [[], []]}, {"x": [[1], [2]]}]),
])
def test_nested_arrays_in_inline_tables(value, expected):
    assert toml.loads("[a]\nb = " + value) == {"a": {"b": expected}}
    document = "a = {before = 1, b = " + value + ", after = 2}"
    assert toml.loads(document) == {
        "a": {"before": 1, "b": expected, "after": 2}}


@pytest.mark.parametrize("value", ["[]", "[1, 2]", '["a,b", "c"]'])
def test_flat_inline_arrays_match_regular_tables(value):
    assert toml.loads("a = {b = " + value + "}") == toml.loads(
        "[a]\nb = " + value)


@pytest.mark.parametrize("value", ["[[1], [2]", "[[1}, [2]]", "[1], [2]"])
def test_invalid_nested_inline_arrays(value):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads("a = {b = " + value + "}")
