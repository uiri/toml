import toml
import pytest
import os


TEST_STR = """
[a]
b = 1
c = 2
"""

TEST_DICT = {"a": {"b": 1, "c": 2}}


def test_bug_148():
    assert 'a = "\\u0064"\n' == toml.dumps({'a': '\\x64'})
    assert 'a = "\\\\x64"\n' == toml.dumps({'a': '\\\\x64'})
    assert 'a = "\\\\\\u0064"\n' == toml.dumps({'a': '\\\\\\x64'})


def test_valid_tests():
    valid_dir = "toml-test/tests/valid/"
    for f in os.listdir(valid_dir):
        if not f.endswith("toml"):
            continue
        toml.dumps(toml.load(open(os.path.join(valid_dir, f))))


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


def test_invalid_tests():
    invalid_dir = "toml-test/tests/invalid/"
    for f in os.listdir(invalid_dir):
        if not f.endswith("toml"):
            continue
        with pytest.raises(toml.TomlDecodeError):
            toml.load(open(os.path.join(invalid_dir, f)))


def test_exceptions():
    with pytest.raises(TypeError):
        toml.loads(2)

    with pytest.raises(TypeError):
        toml.load(2)

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
    o = toml.loads(toml.dumps(TEST_DICT))
    assert o == toml.loads(toml.dumps(o))
