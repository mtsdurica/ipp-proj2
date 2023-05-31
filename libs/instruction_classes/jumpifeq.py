"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *


class Jumpifeq(Instruction):
    def __init__(self, order):
        super().__init__(order, 'JUMPIFEQ')

    def check_num_of_args(self):
        if len(self._args) != 3:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        j_label_id = self.get_args()[0].get_val()
        j_order = self.get_order()
        symb1_val, symb1_frame, symb1_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val())
        symb2_val, symb2_frame, symb2_type = get_symb(
            self.get_args()[2].get_type(), self.get_args()[2].get_val())
        # getting type and value of symbols if they are variables
        if symb1_type == 'var':
            tmp = get_from_frame(
                symb1_frame, symb1_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            symb1_type = tmp.get_type()
            symb1_val = tmp.get_val()

        if symb2_type == 'var':
            tmp = get_from_frame(
                symb2_frame, symb2_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            symb2_type = tmp.get_type()
            symb2_val = tmp.get_val()

        if symb1_type == symb2_type or symb1_type == 'nil' or symb2_type == 'nil':
            label = find_label(
                instructions, j_label_id, j_order, labels)
            # returning iterator with the new value to correctly jump
            if symb1_val == symb2_val:
                return iter(instructions[label:])
        else:
            errprint('Operands not of the same type!')
            exit(53)
