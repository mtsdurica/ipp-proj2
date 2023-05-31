"""
Author: Matúš Ďurica (xduric06)
"""


from libs.argument import Argument
from .utils import *


class Instruction:
    def __init__(self, order, opcode):
        self._opcode = opcode
        self._order = order
        self._args = []

    def add_arg(self, arg_type, arg_val, arg_order):
        arg_order = arg_order[3:]
        self._args.append(Argument(arg_type, arg_val, arg_order))
        self._args = sorted(self._args, key=lambda x: x.get_order())

    def get_opcode(self) -> str:
        return self._opcode

    def get_order(self) -> int:
        return self._order

    def set_order(self, new):
        self._order = new

    def get_args(self) -> list:
        return self._args

    def check_num_of_args(self):
        if len(self._args) > 0:
            errprint('Too many arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        """
        Mainly forward declaration for overriding, no real functionality provided

        """
        return
