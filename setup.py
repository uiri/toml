from distutils.core import setup
from sys import version_info

with open("README.md") as readmefile:
    readme = readmefile.read()

dependencies = []

if version_info < (2, 7):
    dependencies.append('ordereddict')

setup(name='toml',
      version='0.6.5',
      description="Python Library for Tom's Obvious, Minimal Language",
      author="Uiri Noyb",
      author_email="uiri@xqz.ca",
      url="https://github.com/uiri/toml",
      py_modules=['toml'],
      license="License :: OSI Approved :: MIT License",
      long_description=readme,
      requires=dependencies
)
