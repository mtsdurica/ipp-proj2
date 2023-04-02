from ..instruction import Instruction
from ..utils import *


class Add(Instruction):
    def __init__(self, order):
        super().__init__(order, 'ADD')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        symb1_val, symb1_frame, symb1_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val())
        symb2_val, symb2_frame, symb2_type = get_symb(
            self.get_args()[2].get_type(), self.get_args()[2].get_val())

        if symb1_type == 'var' and symb2_type == 'int':
            tmp = GF_vars.get(symb1_val).get_val()
            sum = tmp + symb2_val
            updated = GF_vars.get(var_id)
            updated.set_val(sum)
            updated.set_type('int')
            GF_vars.update({var_id: updated})
