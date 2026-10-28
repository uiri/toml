import datetime

import pytest

import toml


@pytest.mark.parametrize('fraction, microsecond', [
    ('1', 100000),
    ('000001', 1),
    ('123456', 123456),
    ('123456789', 123456),
    ('9999999999999999', 999999),
    ('123456999999999999', 123456),
    ('000000999999999999', 0),
    ('9' * 400, 999999),
])
@pytest.mark.parametrize('offset, delta', [
    ('', None),
    ('Z', datetime.timedelta(0)),
    ('+05:30', datetime.timedelta(hours=5, minutes=30)),
    ('-07:00', -datetime.timedelta(hours=7)),
])
def test_datetime_fraction_truncates_to_microseconds(
        fraction, microsecond, offset, delta):
    source = 'value = 1979-05-27T07:32:00.' + fraction + offset

    value = toml.loads(source)['value']

    assert value.replace(tzinfo=None) == datetime.datetime(
        1979, 5, 27, 7, 32, 0, microsecond)
    assert value.utcoffset() == delta
