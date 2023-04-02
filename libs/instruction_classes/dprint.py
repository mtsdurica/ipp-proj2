from ..instruction import Instruction
from ..utils import *
import sys


class Dprint(Instruction):
    def __init__(self, order):
        super().__init__(order, 'DPRINT')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        # TODO: rest of cases
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[0].get_type(), self.get_args()[0].get_val())
        match symb_type:
            case 'var':
                out = get_from_frame(symb_frame, symb_val,
                                     GF_vars, TF_vars, LF_stack)
                if out.get_type() == 'string':
                    print(parse_esc_seq(out.get_val()),
                          end='', file=sys.stderr)
                elif out.get_type() == 'nil':
                    print(out.get_val(), file=sys.stderr)
                else:
                    print(out.get_val(), end='',
                          file=sys.stderr)
            case 'string':
                print(parse_esc_seq(out.get_val()),
                      end='', file=sys.stderr)
            case 'int' | 'bool' | 'nil':
                print(symb_val, end='', file=sys.stderr)
