"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *


class Read(Instruction):
    def __init__(self, order):
        super().__init__(order, 'READ')

    def check_num_of_args(self):
        if len(self._args) != 2:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        var_id, var_frame, _ = get_var(self.get_args()[0].get_val())
        check_var(var_frame, var_id, TF_created_flag,
                  GF_vars, TF_vars, LF_stack)
        read_type = self.get_args()[1].get_val()

        if not input_file_flag:
            line = input()
        else:
            line = args.input.readline().rstrip()
        var = get_from_frame(
            var_frame, var_id, TF_created_flag, GF_vars, TF_vars, LF_stack)
        var.set_val(conv_to_correct(line, read_type))
        if var.get_val() == 'nil':
            var.set_type('nil')
        else:
            var.set_type(read_type)
        update_in_frame(var_frame, var_id, var, GF_vars, TF_vars, LF_stack)
