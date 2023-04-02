from ..instruction import Instruction
from ..utils import *


class Jumpifneq(Instruction):
    def __init__(self, order):
        super().__init__(order, 'JUMPIFNEQ')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        j_label_id = self.get_args()[0].get_val()
        j_order = self.get_order()
        symb1_val, symb1_frame, symb1_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val())
        symb2_val, symb2_frame, symb2_type = get_symb(
            self.get_args()[2].get_type(), self.get_args()[2].get_val())
        # getting type and value of symbols if they are variables
        if symb1_type == 'var':
            tmp = get_from_frame(
                symb1_frame, symb1_val, GF_vars, TF_vars, LF_stack)
            symb1_type = tmp.get_type()
            symb1_val = tmp.get_val()
        if symb2_type == 'var':
            tmp = get_from_frame(
                symb2_frame, symb2_val, GF_vars, TF_vars, LF_stack)
            symb2_type = tmp.get_type()
            symb2_val = tmp.get_val()
        # TODO: add null
        if symb1_type == symb2_type and symb1_val != symb2_val:
            label = find_label(
                instructions, j_label_id, j_order, labels)
            # returning iterator with the new value to correctly jump
            return iter(instructions[label-1:])
