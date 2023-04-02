from ..instruction import Instruction
from ..utils import *


class Read(Instruction):
    def __init__(self, order):
        super().__init__(order, 'READ')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        var_id, var_frame, var_type = get_var(self.get_args()[0].get_val())
        type = self.get_args()[1].get_val()
        match var_frame:
            case 'GF':
                if not input_file_flag:
                    line = input()
                else:
                    with open(args.input) as f:
                        line = f.readline().rstrip()
                tmp = GF_vars.get(var_id)
                tmp.set_val(conv_to_correct(line, type))
                tmp.set_type(type)
                GF_vars.update({var_id: tmp})
            case 'TF':
                if not input_file_flag:
                    line = input()
                else:
                    with open(args.input) as f:
                        line = f.readline().rstrip()
                tmp = TF_vars.get(var_id)
                tmp.set_val(conv_to_correct(line, type))
                tmp.set_type(type)
                TF_vars.update({var_id: tmp})
            case 'LF':
                if not input_file_flag:
                    line = input()
                else:
                    with open(args.input) as f:
                        line = f.readline().rstrip()
                tmp = get_from_stack(LF_stack, var_id)
                tmp.set_val(conv_to_correct(line, type))
                tmp.set_type(type)
                update_on_stack(LF_stack, var_id, tmp)
