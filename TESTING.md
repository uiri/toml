There is a toml_test.py script which acts as a harness in order to allow toml to be used with [BurntSushi's toml test suite](https://github.com/BurntSushi/toml-test), written in Go. Usage means installing go, the toml-test suite and running the toml-test go binary with toml_test.py as its argument. Modification of tests should happen in BurntSushi's repository. For testing python3 (rather than python2), the toml_test3.py script should be used instead.