import toml
import pytest


TEST_STR = """
[a]
b = 1
c = 2
"""

INVALID_TOML = """
strings-and-ints = ["hi", 42]
"""

TEST_DICT = {"a": {"b": 1, "c": 2}}


def test_simple_str():
    o = toml.loads(TEST_STR)
    assert o == toml.loads(toml.dumps(o))


def test_dict_decoder():
    class TestDict(dict):
        pass

    test_dict_decoder = toml.TomlDecoder(TestDict)
    assert isinstance(toml.loads(
        TEST_STR, decoder=test_dict_decoder), TestDict)


def test_exceptions():
    with pytest.raises(TypeError):
        toml.loads(2)

    with pytest.raises(TypeError):
        toml.load(2)

    with pytest.raises(toml.TomlDecodeError):
        toml.loads(toml.loads(INVALID_TOML))

    try:
        FileNotFoundError
    except NameError:
        # py2
        FileNotFoundError = IOError

    with pytest.raises(FileNotFoundError):
        toml.load([])


def test_warnings():
    # Expect 1 warning for the non existent toml file
    with pytest.warns(UserWarning):
        toml.load(["test.toml", "nonexist.toml"])


def test_commutativity():
    string = toml.dumps(TEST_DICT)
    assert string == toml.dumps(toml.loads(string))
