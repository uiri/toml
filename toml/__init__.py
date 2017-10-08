"""Python module which parses and emits TOML.

Released under the MIT license.
"""

from toml import encoder
from toml import decoder

__version__ = "0.10.0"
__spec__ = "0.4.0"

load = decoder.load
loads = decoder.loads
TomlDecoder = decoder.TomlDecoder

dump = encoder.dump
dumps = encoder.dumps

TomlDecodeError = decoder.TomlDecodeError
