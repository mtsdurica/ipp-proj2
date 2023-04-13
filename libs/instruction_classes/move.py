from ..instruction import Instruction
from ..utils import *


class Move(Instruction):
    def __init__(self, order):
        super().__init__(order, 'MOVE')

    def check_num_of_args(self):
        if len(self._args) != 2:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val()
        )
        _ = get_from_frame(
            var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
        if not symb_frame:
            updated = get_from_frame(
                var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
            updated.set_val(symb_val)
            updated.set_type(symb_type)
        else:
            _ = get_from_frame(
                symb_frame, symb_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            check_var(symb_frame, symb_val, symb_type,
                      GF_vars, TF_vars, LF_stack)
            updated = get_from_frame(
                symb_frame, symb_val, TF_created_flag, GF_vars, TF_vars, LF_stack)
            if not updated.get_val():
                exit(56)
        update_in_frame(var_frame, var_id, updated, GF_vars, TF_vars, LF_stack)
