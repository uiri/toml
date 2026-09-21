import pytest

import toml


@pytest.mark.parametrize('value', [
    {'a': [{'name': 'bob', 'kwargs': {}}]},
    {'a': [{'kwargs': {}}, {'kwargs': {}}]},
    {'a': [{'nested': {'empty': {}}, 'name': 'bob'}]},
    {'a': [{'quoted key': {'quoted.child': {}}}]},
])
def test_empty_subtables_survive_array_of_tables_round_trip(value):
    assert toml.loads(toml.dumps(value)) == value
