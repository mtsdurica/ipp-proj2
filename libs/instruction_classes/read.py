from ..instruction import Instruction
from ..utils import *


class Read(Instruction):
    def __init__(self, order):
        super().__init__(order, 'READ')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, _ = get_var(self.get_args()[0].get_val())
        check_var(var_frame, var_id, None, GF_vars, TF_vars, LF_stack)
        read_type = self.get_args()[1].get_val()

        if not input_file_flag:
            line = input()
        else:
            with open(args.input) as f:
                line = f.readline().rstrip()
        var = get_from_frame(var_frame, var_id, GF_vars, TF_vars, LF_stack)
        var.set_val(conv_to_correct(line, read_type))
        var.set_type(read_type)
        update_in_frame(var_frame, var_id, var, GF_vars, TF_vars, LF_stack)
