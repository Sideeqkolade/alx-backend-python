#!/usr/bin/env python3
""" A script that returns the sum of a list as a float
"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """ a type-annotated function sum_list which takes a list
        input_list of floats as argument and returns their sum
        as a float.
    """

    result = 0

    for i in input_list:
        result = result + i
    return result
