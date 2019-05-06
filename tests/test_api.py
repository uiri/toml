import toml
import copy
import pytest
import os
import sys
from decimal import Decimal

from toml.decoder import InlineTableDict


TEST_STR = """
[a]\r
b = 1\r
c = 2
"""

TEST_DICT = {"a": {"b": 1, "c": 2}}


def test_bug_148():
    assert 'a = "\\u0064"\n' == toml.dumps({'a': '\\x64'})
    assert 'a = "\\\\x64"\n' == toml.dumps({'a': '\\\\x64'})
    assert 'a = "\\\\\\u0064"\n' == toml.dumps({'a': '\\\\\\x64'})


def test_bug_144():
    if sys.version_info >= (3,):
        return

    bug_dict = {'username': '\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d'}
    round_trip_bug_dict = toml.loads(toml.dumps(bug_dict))
    unicoded_bug_dict = {'username': bug_dict['username'].decode('utf-8')}
    assert round_trip_bug_dict == unicoded_bug_dict
    assert bug_dict['username'] == (round_trip_bug_dict['username']
                                    .encode('utf-8'))


def test_bug_196():
    import datetime
    d = datetime.datetime.now()
    bug_dict = {'x': d}
    round_trip_bug_dict = toml.loads(toml.dumps(bug_dict))
    assert round_trip_bug_dict == bug_dict
    assert round_trip_bug_dict['x'] == bug_dict['x']


def test_valid_tests():
    valid_dir = "toml-test/tests/valid/"
    for f in os.listdir(valid_dir):
        if not f.endswith("toml"):
            continue
        with open(os.path.join(valid_dir, f)) as fh:
            toml.dumps(toml.load(fh))


def test_circular_ref():
    a = {}
    b = {}
    b['c'] = 4
    b['self'] = b
    a['b'] = b
    with pytest.raises(ValueError):
        toml.dumps(a)

    with pytest.raises(ValueError):
        toml.dumps(b)


def test__dict():
    class TestDict(dict):
        pass

    assert isinstance(toml.loads(
        TEST_STR, _dict=TestDict), TestDict)


def test_dict_decoder():
    class TestDict(dict):
        pass

    test_dict_decoder = toml.TomlDecoder(TestDict)
    assert isinstance(toml.loads(
        TEST_STR, decoder=test_dict_decoder), TestDict)


def test_inline_dict():
    class TestDict(dict, InlineTableDict):
        pass

    encoder = toml.TomlPreserveInlineDictEncoder()
    t = copy.deepcopy(TEST_DICT)
    t['d'] = TestDict()
    t['d']['x'] = "abc"
    o = toml.loads(toml.dumps(t, encoder=encoder))
    assert o == toml.loads(toml.dumps(o, encoder=encoder))


def test_array_sep():
    encoder = toml.TomlArraySeparatorEncoder(separator=",\t")
    d = {"a": [1, 2, 3]}
    o = toml.loads(toml.dumps(d, encoder=encoder))
    assert o == toml.loads(toml.dumps(o, encoder=encoder))


def test_numpy_floats():
    import numpy as np

    encoder = toml.TomlNumpyEncoder()
    d = {'a': np.array([1, .3], dtype=np.float64)}
    o = toml.loads(toml.dumps(d, encoder=encoder))
    assert o == toml.loads(toml.dumps(o, encoder=encoder))

    d = {'a': np.array([1, .3], dtype=np.float32)}
    o = toml.loads(toml.dumps(d, encoder=encoder))
    assert o == toml.loads(toml.dumps(o, encoder=encoder))

    d = {'a': np.array([1, .3], dtype=np.float16)}
    o = toml.loads(toml.dumps(d, encoder=encoder))
    assert o == toml.loads(toml.dumps(o, encoder=encoder))


def test_ordered():
    from toml import ordered as toml_ordered
    encoder = toml_ordered.TomlOrderedEncoder()
    decoder = toml_ordered.TomlOrderedDecoder()
    o = toml.loads(toml.dumps(TEST_DICT, encoder=encoder), decoder=decoder)
    assert o == toml.loads(toml.dumps(TEST_DICT, encoder=encoder),
                           decoder=decoder)


def test_tuple():
    d = {"a": (3, 4)}
    o = toml.loads(toml.dumps(d))
    assert o == toml.loads(toml.dumps(o))


def test_decimal():
    PLACES = Decimal(10) ** -4

    d = {"a": Decimal("0.1")}
    o = toml.loads(toml.dumps(d))
    assert o == toml.loads(toml.dumps(o))
    assert Decimal(o["a"]).quantize(PLACES) == d["a"].quantize(PLACES)


def test_invalid_tests():
    invalid_dir = "toml-test/tests/invalid/"
    for f in os.listdir(invalid_dir):
        if not f.endswith("toml"):
            continue
        with pytest.raises(toml.TomlDecodeError):
            with open(os.path.join(invalid_dir, f)) as fh:
                toml.load(fh)


def test_exceptions():
    with pytest.raises(TypeError):
        toml.loads(2)

    with pytest.raises(TypeError):
        toml.load(2)

    try:
        FNFError = FileNotFoundError
    except NameError:
        # py2
        FNFError = IOError

    with pytest.raises(FNFError):
        toml.load([])


class FakeFile(object):

    def __init__(self):
        self.written = ""

    def write(self, s):
        self.written += s
        return None

    def read(self):
        return self.written


def test_dump():
    from collections import OrderedDict
    f = FakeFile()
    g = FakeFile()
    h = FakeFile()
    toml.dump(TEST_DICT, f)
    toml.dump(toml.load(f, _dict=OrderedDict), g)
    toml.dump(toml.load(g, _dict=OrderedDict), h)
    assert g.written == h.written


def test_paths():
    toml.load("test.toml")
    import sys
    if (3, 4) <= sys.version_info:
        import pathlib
        p = pathlib.Path("test.toml")
        toml.load(p)


def test_warnings():
    # Expect 1 warning for the non existent toml file
    with pytest.warns(UserWarning):
        toml.load(["test.toml", "nonexist.toml"])


def test_commutativity():
    o = toml.loads(toml.dumps(TEST_DICT))
    assert o == toml.loads(toml.dumps(o))
