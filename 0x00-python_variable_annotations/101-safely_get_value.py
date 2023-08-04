#!/usr/bin/env python3
""" A script of Annonated function module
"""
from typing import Union, Mapping, Any, T


def safely_get_value(dct: Mapping, key: Any, default: Union[T, None]) -> \
                     Union[Any, T]:
    """add type annotations to the function"""
    if key in dct:
        return dct[key]
    else:
        return default
