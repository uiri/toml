import datetime

import pytest

import toml


@pytest.mark.parametrize('fraction, microsecond', [
    ('1', 100000), ('12', 120000), ('123', 123000), ('1234', 123400),
    ('12345', 123450), ('123456', 123456), ('1234567', 123456),
    ('000001', 1), ('0000009', 0),
])
def test_local_time_fraction(fraction, microsecond):
    document = 'time = 12:34:56.' + fraction
    expected = {'time': datetime.time(12, 34, 56, microsecond)}
    assert toml.loads(document) == expected
    assert pytest.importorskip('tomllib').loads(document) == expected


@pytest.mark.parametrize('value', ['12:34:56.', '12:34:56.1oops',
                                   '12:34:56garbage'])
def test_invalid_local_time(value):
    with pytest.raises(toml.TomlDecodeError):
        toml.loads('time = ' + value)
