from ..instruction import Instruction
from ..utils import *


class Exit(Instruction):
    def __init__(self, order):
        super().__init__(order, 'EXIT')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[0].get_type(), self.get_args()[0].get_val())
        if symb_type == 'var':
            tmp = get_from_frame(
                symb_frame, symb_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            check_var(symb_frame, symb_val, TF_created_flag,
                      GF_vars, TF_vars, LF_stack)
            symb_type = tmp.get_type()
            symb_val = tmp.get_val()
        if symb_type == 'int':
            if symb_val >= 0 and symb_val <= 49:
                exit(symb_val)
            else:
                errprint('Bad exit code!')
                exit(57)
        else:
            errprint('Bad type!')
            exit(53)
