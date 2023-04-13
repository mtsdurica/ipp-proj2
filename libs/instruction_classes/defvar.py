from ..instruction import Instruction
from ..variable import Variable
from ..utils import *


class Defvar(Instruction):
    def __init__(self, order):
        super().__init__(order, 'DEFVAR')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        var_id, var_frame, _ = get_var(self.get_args()[0].get_val())
        var_obj = Variable(var_id)

        match var_frame:
            case 'GF':
                if GF_vars.get(var_id):
                    exit(52)
            case 'TF':
                if TF_vars.get(var_id):
                    exit(52)
            case 'LF':
                if get_from_stack(LF_stack, var_id):
                    exit(52)

        if var_frame == 'TF' and not TF_created_flag:
            errprint('Creating variable on not existing frame attempted!')
            exit(55)
        update_in_frame(var_frame, var_id, var_obj, GF_vars, TF_vars, LF_stack)
