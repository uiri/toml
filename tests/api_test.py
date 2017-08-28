if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.insert(0, path.dirname(path.dirname(__file__)))

from toml import TomlDecodeError  # noqa: E402
import toml  # noqa: E402
import warnings  # noqa: E402


class TestDict(dict):
    pass


try:
    FNFError = FileNotFoundError
except NameError:
    FNFError = IOError


TEST_STR = """
[a]
b = 1
c = 2
"""

INVALID_TOML = """
strings-and-ints = ["hi", 42]
"""

TEST_DICT = {"a": {"b": 1, "c": 2}}

o = toml.loads(TEST_STR)
assert(o == toml.loads(toml.dumps(o)))
assert(isinstance(toml.loads(TEST_STR, _dict=TestDict), TestDict))

try:
    toml.loads(2)
    # Expected TypeError
    assert(False)
except TypeError:
    pass

try:
    toml.loads(INVALID_TOML)
    # Expected TomlDecodeError
    assert(False)
except TomlDecodeError:
    pass

try:
    toml.load(2)
    # Expected TypeError
    assert(False)
except TypeError:
    pass

try:
    toml.load([])
    # Expected FileNotFoundError or IOError (according to Python version)
    assert(False)
except FNFError:
    pass

toml.load(["test.toml"])

with warnings.catch_warnings(record=True) as w:
    toml.load(["test.toml", "nonexist.toml"])
    # Expect 1 warning for the non existent toml file
    assert(len(w) == 1)

s = toml.dumps(TEST_DICT)
assert(s == toml.dumps(toml.loads(s)))
