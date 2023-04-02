from libs.argument import Argument


class Instruction:
    def __init__(self, order, opcode):
        self._opcode = opcode
        self._order = order
        self._args = []

    def add_arg(self, arg_type, arg_val):
        self._args.append(Argument(arg_type, arg_val))

    def get_opcode(self) -> str:
        return self._opcode

    def get_order(self) -> int:
        return self._order

    def get_args(self) -> list:
        return self._args
