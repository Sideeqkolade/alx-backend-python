#!/usr/bin/env python3
""" A script that returns a function that multiplies a float
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    return (lambda a: a * multiplier)
