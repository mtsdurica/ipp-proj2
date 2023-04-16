from ..instruction import Instruction
from ..utils import *


class Setchar(Instruction):
    def __init__(self, order):
        super().__init__(order, 'SETCHAR')

    def check_num_of_args(self):
        if len(self._args) != 3:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        check_var(var_frame, var_id, TF_created_flag,
                  GF_vars, TF_vars, LF_stack)

        symb1_val, symb1_frame, symb1_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val())

        symb2_val, symb2_frame, symb2_type = get_symb(
            self.get_args()[2].get_type(), self.get_args()[2].get_val())

        if symb1_type == 'var':
            tmp = get_from_frame(
                symb1_frame, symb1_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            check_var(symb1_frame, symb1_val, TF_created_flag,
                      GF_vars, TF_vars, LF_stack)
            symb1_type = tmp.get_type()
            symb1_val = tmp.get_val()

        if symb2_type == 'var':
            tmp = get_from_frame(
                symb2_frame, symb2_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not tmp.get_type():
                errprint('uninit var')
                exit(56)
            check_var(symb2_frame, symb2_val, TF_created_flag,
                      GF_vars, TF_vars, LF_stack)
            symb2_type = tmp.get_type()
            symb2_val = tmp.get_val()

        tmp = get_from_frame(
            var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
        var_type = tmp.get_type()

        if var_type == 'string' and symb1_type == 'int' and symb2_type == 'string':
            try:
                if int(symb1_val) >= 0:
                    updated = get_from_frame(
                        var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
                    updated_val = updated.get_val()
                    if int(symb1_val) > len(updated_val)-1:
                        errprint('Out of range!')
                        exit(58)
                    updated_val = updated_val[:symb1_val] + \
                        symb2_val[0] + updated_val[symb1_val+1:]
                    updated.set_val(updated_val)
                    updated.set_type('string')
                else:
                    exit(58)
            except IndexError:
                errprint('Out of range!')
                exit(58)
        else:
            errprint('Bad type!')
            exit(53)

        update_in_frame(var_frame, var_id, updated, GF_vars, TF_vars, LF_stack)
