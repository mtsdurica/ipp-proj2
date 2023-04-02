from ..instruction import Instruction
from ..utils import *


class Move(Instruction):
    def __init__(self, order):
        super().__init__(order, 'MOVE')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[1].get_type(), self.get_args()[1].get_val()
        )

        if not symb_frame:
            updated = get_from_frame(
                var_frame, var_id, GF_vars, TF_vars, LF_stack)
            updated.set_val(symb_val)
            updated.set_type(symb_type)
        else:
            updated = get_from_frame(
                symb_frame, symb_val, GF_vars, TF_vars, LF_stack
            )
        update_in_frame(var_frame, var_id, updated, GF_vars, TF_vars, LF_stack)
