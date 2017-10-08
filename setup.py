try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import toml

with open("README.rst") as readme_file:
    readme_string = readme_file.read()

setup(
    name="toml",
    version=toml.__version__,
    description="Python Library for Tom's Obvious, Minimal Language",
    author="Uiri Noyb",
    author_email="uiri@xqz.ca",
    url="https://github.com/uiri/toml",
    packages=['toml'],
    license="License :: OSI Approved :: MIT License",
    long_description=readme_string,
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6']
)
