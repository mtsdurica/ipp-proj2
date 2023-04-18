"""
Author: Matúš Ďurica (xduric06)
"""


class Argument:
    def __init__(self, arg_type, arg_val, arg_order):
        self._type = arg_type
        self._val = arg_val
        self._order = arg_order

    def get_type(self) -> str:
        return self._type

    def get_val(self) -> str | int:
        return self._val

    def get_order(self) -> int:
        return self._order
