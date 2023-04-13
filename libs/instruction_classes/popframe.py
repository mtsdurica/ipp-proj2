from ..instruction import Instruction
from ..utils import *


class Popframe(Instruction):
    def __init__(self, order):
        super().__init__(order, 'POPFRAME')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        TF_vars.clear()
        try:
            TF_vars.update(LF_stack.pop())
        except IndexError:
            errprint('Popping from empty LF stack attempted!')
            exit(55)
