import os

import pytest


@pytest.fixture(scope='session')
def tests_dir():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def toml_test_dir(tests_dir):
    return os.path.join(tests_dir, 'toml-test', 'tests')


@pytest.fixture(scope='session')
def valid_dir(toml_test_dir):
    return os.path.join(toml_test_dir, 'valid')


@pytest.fixture(scope='session')
def invalid_dir(toml_test_dir):
    return os.path.join(toml_test_dir, 'invalid')
