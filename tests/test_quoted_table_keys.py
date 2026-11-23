# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

import toml


@pytest.mark.parametrize('array', [False, True])
@pytest.mark.parametrize('quoted,key', [
    (r'"a\"b"', 'a"b'),
    (r'"a\".b"', 'a".b'),
    (r'"a\"].b"', 'a"].b'),
    (r'"C:\\Program Files\\example"', 'C:\\Program Files\\example'),
    (r'"ends\\"', 'ends\\'),
    (r'"line\nnext"', 'line\nnext'),
    (r'"tab\tkey"', 'tab\tkey'),
    (r'"\u0061.\U0001F680"', 'a.\U0001f680'),
    (r"'literal\q.b'", 'literal\\q.b'),
    ("'a\"quote].b'", 'a"quote].b'),
])
def test_quoted_table_names_decode_once_and_round_trip(quoted, key, array):
    brackets = ('[[', ']]') if array else ('[', ']')
    source = brackets[0] + 'parent.' + quoted + '.child' + brackets[1]
    source += '\nvalue = 42\n'
    child = [{'value': 42}] if array else {'value': 42}
    expected = {'parent': {key: {'child': child}}}
    decoded = toml.loads(source)
    assert decoded == expected
    for _ in range(3):
        decoded = toml.loads(toml.dumps(decoded))
        assert decoded == expected


def test_cargo_target_expression_keeps_its_quotes():
    source = (
        r'[target."cfg(all(target_arch = \"wasm32\", '
        r'not(any(target_os = \"emscripten\", target_os = \"wasi\"))))"'
        '.dependencies.wasm-bindgen]\n'
        'version = "0.2"\noptional = true\n'
    )
    target = ('cfg(all(target_arch = "wasm32", not(any(target_os = '
              '"emscripten", target_os = "wasi"))))')
    expected = {'target': {target: {'dependencies': {
        'wasm-bindgen': {'version': '0.2', 'optional': True}}}}}
    assert toml.loads(source) == expected
    assert toml.loads(toml.dumps(expected)) == expected


@pytest.mark.parametrize('header', [
    r'["bad\q"]', r'["bad\uZZZZ"]', '["name" extra]',
    '["name"] extra', '[parent..child]',
])
def test_invalid_quoted_headers_report_decode_errors(header):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads(header + '\nvalue = 1\n')


def test_escaped_aliases_do_not_create_duplicate_tables():
    with pytest.raises(toml.TomlDecodeError):
        toml.loads('["\\u0061"]\nfirst = 1\n[a]\nsecond = 2\n')
