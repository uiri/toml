import pytest

import toml


@pytest.mark.parametrize('source, expected', [
    ('["foo", {include-group="foo"}, "bar"]',
     ["foo", {"include-group": "foo"}, "bar"]),
    ('["foo", {include-group="foo"}]',
     ["foo", {"include-group": "foo"}]),
    ('["/usr/bin/ping -c4 8.8.8.8", ["packets", "rtt"]]',
     ["/usr/bin/ping -c4 8.8.8.8", ["packets", "rtt"]]),
    ('[{key="value"}, "foo",]', [{"key": "value"}, "foo"]),
    ('["foo", {key="value"},]', ["foo", {"key": "value"}]),
    ('[1, "a", true, 2.5]', [1, "a", True, 2.5]),
    ('[[1, 2], "a,b", {key="x,y"}]', [[1, 2], "a,b", {"key": "x,y"}]),
    ('["a,b", 1, "c,d"]', ["a,b", 1, "c,d"]),
    ("['a,b', 1, 'c,d']", ["a,b", 1, "c,d"]),
    ('["[}]{", {key="[}]"}, []]', ["[}]{", {"key": "[}]"}, []]),
    ('[{nested={key="value"}}, 2]', [{"nested": {"key": "value"}}, 2]),
    ('["a\\\"b,c", [1, 2]]', ['a"b,c', [1, 2]]),
    ('["""a,b""", [1, 2]]', ['a,b', [1, 2]]),
    ("['''a,b''', [1, 2]]", ['a,b', [1, 2]]),
    ('[[], {}, "", 0, false]', [[], {}, "", 0, False]),
    ('[]', []),
])
def test_mixed_array_elements(source, expected):
    assert toml.loads('values = ' + source)['values'] == expected


def test_dependency_groups():
    source = '''
[dependency-groups]
foo = []
bar = ["foo", { include-group = "foo" }, "bar"]
baz = ["foo", { include-group = "foo" }]
'''
    assert toml.loads(source) == {
        'dependency-groups': {
            'foo': [],
            'bar': ['foo', {'include-group': 'foo'}, 'bar'],
            'baz': ['foo', {'include-group': 'foo'}],
        },
    }
