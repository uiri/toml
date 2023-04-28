import toml_tools
import copy
import pytest
import os
import sys
from decimal import Decimal

from toml_tools.decoder import InlineTableDict



TEST_STR = """
[a]\r
b = 1\r
c = 2
"""

TEST_DICT = {"a": {"b": 1, "c": 2}}

def make_bug_148_test_function(toml_module):
    def test_bug_148():
        assert r'a = "\\x64"' + '\n' == toml_module.dumps({'a': r'\x64'})
        assert r'a = "\\\\x64"' + '\n' == toml_module.dumps({'a': r'\\x64'})
        assert r'a = "\\\\\\x64"' + '\n' == toml_module.dumps({'a': r'\\\x64'})

    # original from  
    #     assert 'a = "\\u0064"\n' == toml_module.dumps({'a': '\\x64'})
    #     assert 'a = "\\\\x64"\n' == toml_module.dumps({'a': '\\\\x64'})
    #     assert 'a = "\\\\\\u0064"\n' == toml_module.dumps({'a': '\\\\\\x64'})
    return test_bug_148

test_bug_148_toml_tools = make_bug_148_test_function(toml_tools)

@pytest.skip()
# @pytest.mark.skipif(sys.version_info >= (3,), reason = 'Python 2 only test')
def test_bug_144():

    bug_dict = {'username': '\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d'}
    round_trip_bug_dict = toml_tools.loads(toml_tools.dumps(bug_dict))
    unicoded_bug_dict = {'username': bug_dict['username'].decode('utf-8')}
    assert round_trip_bug_dict == unicoded_bug_dict
    assert bug_dict['username'] == (round_trip_bug_dict['username']
                                    .encode('utf-8'))


def test_bug_196():
    import datetime
    d = datetime.datetime.now()
    bug_dict = {'x': d}
    round_trip_bug_dict = toml_tools.loads(toml_tools.dumps(bug_dict))
    assert round_trip_bug_dict == bug_dict
    assert round_trip_bug_dict['x'] == bug_dict['x']


TOML_TEST_DIR = r"C:\Users\James\Documents\Coding\repos\toml-test-master\toml-test-master\tests"


def test_valid_tests():
    valid_dir = os.path.join(TOML_TEST_DIR,"valid")
    for f in os.listdir(valid_dir):
        if not f.endswith("toml"):
            continue
        with open(os.path.join(valid_dir, f)) as fh:
            toml_tools.dumps(toml_tools.load(fh))


def test_circular_ref():
    a = {}
    b = {}
    b['c'] = 4
    b['self'] = b
    a['b'] = b
    with pytest.raises(ValueError):
        toml_tools.dumps(a)

    with pytest.raises(ValueError):
        toml_tools.dumps(b)


def test__dict():
    class TestDict(dict):
        pass

    assert isinstance(toml_tools.loads(
        TEST_STR, _dict=TestDict), TestDict)


def test_dict_decoder():
    class TestDict(dict):
        pass

    test_dict_decoder = toml_tools.TomlDecoder(TestDict)
    assert isinstance(toml_tools.loads(
        TEST_STR, decoder=test_dict_decoder), TestDict)


def test_inline_dict():
    class TestDict(dict, InlineTableDict):
        pass

    encoder = toml_tools.TomlPreserveInlineDictEncoder()
    t = copy.deepcopy(TEST_DICT)
    t['d'] = TestDict()
    t['d']['x'] = "abc"
    o = toml_tools.loads(toml_tools.dumps(t, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))


def test_array_sep():
    encoder = toml_tools.TomlArraySeparatorEncoder(separator=",\t")
    d = {"a": [1, 2, 3]}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

@pytest.skip()
def test_numpy_floats():
    np = pytest.importorskip('numpy')

    encoder = toml_tools.TomlNumpyEncoder()
    d = {'a': np.array([1, .3], dtype=np.float64)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

    d = {'a': np.array([1, .3], dtype=np.float32)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

    d = {'a': np.array([1, .3], dtype=np.float16)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

@pytest.skip()
def test_numpy_ints():
    np = pytest.importorskip('numpy')

    encoder = toml_tools.TomlNumpyEncoder()
    d = {'a': np.array([1, 3], dtype=np.int64)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

    d = {'a': np.array([1, 3], dtype=np.int32)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))

    d = {'a': np.array([1, 3], dtype=np.int16)}
    o = toml_tools.loads(toml_tools.dumps(d, encoder=encoder))
    assert o == toml_tools.loads(toml_tools.dumps(o, encoder=encoder))


def test_ordered():
    from toml_tools import ordered as toml_ordered
    encoder = toml_ordered.TomlOrderedEncoder()
    decoder = toml_ordered.TomlOrderedDecoder()
    o = toml_tools.loads(toml_tools.dumps(TEST_DICT, encoder=encoder), decoder=decoder)
    assert o == toml_tools.loads(toml_tools.dumps(TEST_DICT, encoder=encoder),
                           decoder=decoder)


def test_tuple():
    d = {"a": (3, 4)}
    o = toml_tools.loads(toml_tools.dumps(d))
    assert o == toml_tools.loads(toml_tools.dumps(o))


def test_decimal():
    PLACES = Decimal(10) ** -4

    d = {"a": Decimal("0.1")}
    o = toml_tools.loads(toml_tools.dumps(d))
    assert o == toml_tools.loads(toml_tools.dumps(o))
    assert Decimal(o["a"]).quantize(PLACES) == d["a"].quantize(PLACES)


def test_invalid_tests():
    invalid_dir = os.path.join(TOML_TEST_DIR,"invalid")
    for f in os.listdir(invalid_dir):
        if not f.endswith("toml"):
            continue
        with pytest.raises(toml_tools.TomlDecodeError):
            with open(os.path.join(invalid_dir, f)) as fh:
                toml_tools.load(fh)


def test_exceptions():
    with pytest.raises(TypeError):
        toml_tools.loads(2)

    with pytest.raises(TypeError):
        toml_tools.load(2)

    try:
        FNFError = FileNotFoundError
    except NameError:
        # py2
        FNFError = IOError

    with pytest.raises(FNFError):
        toml_tools.load([])


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
    toml_tools.dump(TEST_DICT, f)
    toml_tools.dump(toml_tools.load(f, _dict=OrderedDict), g)
    toml_tools.dump(toml_tools.load(g, _dict=OrderedDict), h)
    assert g.written == h.written


def test_paths():
    toml_tools.load(os.path.join(os.path.dirname(__file__), "test.toml"))
    toml_tools.load(os.path.join(os.path.dirname(__file__), b"test.toml"))
    import sys
    if (3, 4) <= sys.version_info:
        import pathlib
        p = pathlib.Path("test.toml")
        toml_tools.load(p)
        

@pytest.skip()
def test_warnings():
    # Expect 1 warning for the non existent toml file
    with pytest.warns(UserWarning):
        toml_tools.load(["test.toml", "nonexist.toml"])


def test_commutativity():
    o = toml_tools.loads(toml_tools.dumps(TEST_DICT))
    assert o == toml_tools.loads(toml_tools.dumps(o))

@pytest.skip()
# @pytest.mark.skipif(sys.platform == 'win32', 
#                     reason = 'Hardcoded POSIX file path from /uiri/toml')
def test_pathlib():
    if (3, 4) <= sys.version_info:
        import pathlib
        o = {"root": {"path": pathlib.Path("/home/edgy")}}
        test_str = """[root]
path = "/home/edgy"
"""
        assert test_str == toml_tools.dumps(o, encoder=toml_tools.TomlPathlibEncoder())


def test_comment_preserve_decoder_encoder():
    test_str = """[[products]]
name = "Nail"
sku = 284758393
# This is a comment
color = "gray" # Hello World
# name = { first = 'Tom', last = 'Preston-Werner' }
# arr7 = [
#  1, 2, 3
# ]
# lines  = '''
# The first newline is
# trimmed in raw strings.
#   All other whitespace
#   is preserved.
# '''

[animals]
color = "gray" # col
fruits = "apple" # a = [1,2,3]
a = 3
b-comment = "a is 3"
"""

    s = toml_tools.dumps(toml_tools.loads(test_str,
                              decoder=toml_tools.TomlPreserveCommentDecoder()),
                   encoder=toml_tools.TomlPreserveCommentEncoder())

    assert len(s) == len(test_str) and sorted(test_str) == sorted(s)


def test_deepcopy_timezone():
    import copy

    o = toml_tools.loads("dob = 1979-05-24T07:32:00-08:00")
    o2 = copy.deepcopy(o)
    assert o2["dob"] == o["dob"]
    assert o2["dob"] is not o["dob"]
