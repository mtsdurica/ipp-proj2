from ..instruction import Instruction
from ..utils import *


class Strlen(Instruction):
    def __init__(self, order):
        super().__init__(order, 'STRLEN')

    def check_num_of_args(self):
        if len(self._args) != 2:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        var_id, var_frame, _ = get_var(self.get_args()[0].get_val())
        check_var(var_frame, var_id, None, GF_vars, TF_vars, LF_stack)
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val())

        if symb_type == 'var':
            tmp = get_from_frame(
                symb_frame, symb_val, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            check_var(symb_frame, symb_val, tmp.get_type(),
                      GF_vars, TF_vars, LF_stack)
            symb_type = tmp.get_type()
            symb_val = tmp.get_val()

        if symb_type == 'string':
            try:
                updated = get_from_frame(
                    var_frame, var_id, GF_vars, TF_vars, LF_stack)
                updated.set_val(len(str(symb_val)))
                updated.set_type('int')
            except TypeError:
                exit(58)
        else:
            errprint('Bad type!')
            exit(58)

        update_in_frame(var_frame, var_id, updated, GF_vars, TF_vars, LF_stack)
