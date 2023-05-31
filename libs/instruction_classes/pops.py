"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *


class Pops(Instruction):
    def __init__(self, order):
        super().__init__(order, 'POPS')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        if not ds:
            errprint('ERROR: Data stack is empty!')
            exit(56)
        else:
            var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
            updated = get_from_frame(
                var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
            popped = ds.pop()
            tmp = popped.popitem()
            updated_val = tmp[0]
            updated.set_val(updated_val)
            updated_type = tmp[1]
            updated.set_type(updated_type)
            update_in_frame(
                var_frame, var_id, updated, GF_vars, TF_vars, LF_stack)
