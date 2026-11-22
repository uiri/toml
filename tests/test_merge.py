from collections import OrderedDict
import io

import pytest
import toml


def configs(tmpdir, *texts):
    paths = []
    for i, text in enumerate(texts):
        path = tmpdir.join("%d.toml" % i)
        path.write(text)
        paths.append(str(path))
    return paths


def test_nested_merge(tmpdir):
    files = configs(tmpdir, '[server]\nhost = "localhost"\nport = 80\n'
                    '[server.tls]\nenabled = false\ncert = "base.pem"\n',
                    '[server]\nport = 8080\n[server.tls]\nenabled = true\n')
    assert toml.load(files, merged=True) == {
        'server': {'host': 'localhost', 'port': 8080,
                   'tls': {'enabled': True, 'cert': 'base.pem'}}}
    assert toml.load(files) == {
        'server': {'port': 8080, 'tls': {'enabled': True}}}
    assert toml.load(files, merged=False) == toml.load(files)


@pytest.mark.parametrize('before,after,expected', [
    ('value = 1', '[value]\nx = 2', {'value': {'x': 2}}),
    ('[value]\nx = 2', 'value = 1', {'value': 1}),
    ('value = [1, 2]', 'value = [3]', {'value': [3]}),
    ('[[value]]\nx = 1', '[[value]]\ny = 2', {'value': [{'y': 2}]}),
    ('[value]\nx = 1', '[value]', {'value': {'x': 1}}),
])
def test_merge_replacement(tmpdir, before, after, expected):
    assert toml.load(configs(tmpdir, before, after), merged=True) == expected


@pytest.mark.parametrize('options', [
    {'_dict': OrderedDict}, {'decoder': toml.TomlDecoder(OrderedDict)}])
def test_merge_custom_dictionary(tmpdir, options):
    files = configs(tmpdir, '[a]\nx = 1', '[a]\ny = 2', '[a]\nx = 3')
    result = toml.load(files, merged=True, **options)
    assert isinstance(result, OrderedDict)
    assert isinstance(result['a'], OrderedDict)
    assert list(result['a'].items()) == [('x', 3), ('y', 2)]


def test_merge_missing_files(tmpdir):
    files = configs(tmpdir, '[a]\nx = 1')
    files.append(str(tmpdir.join('missing')))
    with pytest.warns(UserWarning):
        assert toml.load(files, merged=True) == {
            'a': {'x': 1}}
    with pytest.raises(IOError):
        toml.load([], merged=True)


def test_merge_single_file(tmpdir):
    files = configs(tmpdir, '[a]\nx = 1')
    assert toml.load(files[0], merged=True) == {'a': {'x': 1}}
    assert toml.load(io.StringIO('[a]\nx = 1'), merged=True) == {
        'a': {'x': 1}}
