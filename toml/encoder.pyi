from toml.decoder import InlineTableDict as InlineTableDict
from typing import Any, Optional

unicode = str

def dump(o: Mapping[str, Any], f: IO[str], encoder: TomlEncoder = ...) -> str: ...
def dumps(o: Mapping[str, Any], encoder: TomlEncoder = ...) -> str: ...

class TomlEncoder:
    preserve: Any = ...
    preserve_list: Any = ...
    dump_funcs: Any = ...
    def __init__(self, _dict: Any = ..., preserve: bool = ..., preserve_list: bool = ...): ...
    def get_empty_table(self): ...
    def dump_list(self, v: Any): ...
    def dump_inline_table(self, section: Any, with_newline: bool = ...): ...
    def dump_inline_table_value(self, section: Any): ...
    def dump_value(self, v: Any): ...
    def dump_sections(self, o: Any, sup: Any): ...

class TomlPreserveInlineDictEncoder(TomlEncoder):
    def __init__(self, _dict: Any = ..., preserve_list: bool = ...) -> None: ...

class TomlArraySeparatorEncoder(TomlEncoder):
    separator: Any = ...
    def __init__(self, _dict: Any = ..., preserve: bool = ..., separator: str = ..., preserve_list: bool = ...) -> None: ...
    def dump_list(self, v: Any): ...

class TomlNumpyEncoder(TomlEncoder):
    def __init__(self, _dict: Any = ..., preserve: bool = ..., preserve_list: bool = ...) -> None: ...

class TomlPreserveCommentEncoder(TomlEncoder):
    def __init__(self, _dict: Any = ..., preserve: bool = ..., preserve_list: bool = ...): ...

class TomlPathlibEncoder(TomlEncoder):
    def dump_value(self, v: Any): ...
