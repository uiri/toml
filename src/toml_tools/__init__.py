"""Python module which parses and emits TOML.

Released under the MIT license.
"""

from . import encoder
from . import decoder


load = decoder.load
loads = decoder.loads
TomlDecoder = decoder.TomlDecoder
TomlDecodeError = decoder.TomlDecodeError
TomlPreserveCommentDecoder = decoder.TomlPreserveCommentDecoder

dump = encoder.dump
dumps = encoder.dumps
TomlEncoder = encoder.TomlEncoder
TomlArraySeparatorEncoder = encoder.TomlArraySeparatorEncoder
TomlPreserveInlineDictEncoder = encoder.TomlPreserveInlineDictEncoder
TomlNumpyEncoder = encoder.TomlNumpyEncoder
TomlPreserveCommentEncoder = encoder.TomlPreserveCommentEncoder
TomlPathlibEncoder = encoder.TomlPathlibEncoder
