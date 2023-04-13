from ..instruction import Instruction
from ..utils import *


class Return(Instruction):
    def __init__(self, order):
        super().__init__(order, 'RETURN')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        label = stack.pop()
        # returning iterator with the new value to correctly jump
        return iter(instructions[label:])
