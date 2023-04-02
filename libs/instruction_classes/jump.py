from ..instruction import Instruction
from ..utils import *


class Jump(Instruction):
    def __init__(self, order):
        super().__init__(order, 'JUMP')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        j_label_id = self.get_args()[0].get_val()
        j_order = self.get_order()
        label = find_label(instructions, j_label_id, j_order, labels)
        # returning iterator with the new value to correctly jump
        return iter(instructions[label:])
