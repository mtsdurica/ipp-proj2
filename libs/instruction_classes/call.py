from ..instruction import Instruction
from ..utils import *


class Call(Instruction):
    def __init__(self, order):
        super().__init__(order, 'CALL')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        j_label_id = self.get_args()[0].get_val()
        j_order = self.get_order()
        label = find_label(instructions, j_label_id, j_order, labels)
        stack.append(j_order)
        # returning iterator with the new value to correctly jump
        return iter(instructions[label:])
