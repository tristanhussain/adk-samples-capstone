import types as builtin_types
import typing

typing._UnionGenericAlias = builtin_types.UnionType  # type: ignore[attr-defined]
