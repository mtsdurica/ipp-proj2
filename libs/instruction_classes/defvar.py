from ..instruction import Instruction
from ..variable import Variable
from ..utils import *


class Defvar(Instruction):
    def __init__(self, order):
        super().__init__(order, 'DEFVAR')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, _ = get_var(self.get_args()[0].get_val())
        var_obj = Variable(var_id)
        check = get_from_frame(var_frame, var_id,  GF_vars, TF_vars, LF_stack)
        if check:
            exit(52)
        update_in_frame(var_frame, var_id, var_obj, GF_vars, TF_vars, LF_stack)
