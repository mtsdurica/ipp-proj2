from ..instruction import Instruction
from ..variable import Variable
from ..utils import *


class Defvar(Instruction):
    def __init__(self, order):
        super().__init__(order, 'DEFVAR')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        var_obj = Variable(var_id)
        match var_frame:
            case 'GF':
                GF_vars.update({var_obj.get_id(): var_obj})
            case 'TF':
                TF_vars.update({var_obj.get_id(): var_obj})
            case 'LF':
                update_on_stack(LF_stack, var_obj.get_id(), var_obj)
