import toml
from distutils.core import setup

with open("README.rst") as readmefile:
    readme = readmefile.read()
setup(name='toml',
      version=toml.__version__,
      description="Python Library for Tom's Obvious, Minimal Language",
      author="Uiri Noyb",
      author_email="uiri@xqz.ca",
      url="https://github.com/uiri/toml",
      py_modules=['toml'],
      license="License :: OSI Approved :: MIT License",
      long_description=readme,
)
