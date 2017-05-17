# Testing
There is a `toml_test.py` script which acts as a harness in order to allow toml to be used with [BurntSushi's toml test suite](https://github.com/BurntSushi/toml-test), written in Go.

## Usage
1. Install Go (golang)
2. The toml-test suite
	1. [Instructions](https://github.com/BurntSushi/toml-test#try-it-out)
3. Execute with either of:
	* `~/go/bin/toml-test ./tests/decoding_test.sh` - Default (PATH) Python version
	* `~/go/bin/toml-test ./tests/decoding_test2.sh` - Python 2
	* `~/go/bin/toml-test ./tests/decoding_test3.sh` - Python 3

## Addendum
There's also two Python test-files in the `./tests` directory
* `example_test.py`,
* and `decoding_test.py`.

Both of which require the `toml` library to be importable (aka `import toml` to work).
Both also require Python 3 (due to using `print()`).
