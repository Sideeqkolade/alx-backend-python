#!/usr/bin/env python3
""" A script that annotate the below function’s parameters
    and return values with the appropriate types
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ a typed-function that returns an iterables
    """
    return [(i, len(i)) for i in lst]
