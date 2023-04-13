from ..instruction import *


class Write(Instruction):
    def __init__(self, order):
        super().__init__(order, 'WRITE')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        symb_val, symb_frame, symb_type = get_symb(
            self.get_args()[0].get_type(), self.get_args()[0].get_val()
        )

        match symb_type:
            case 'var':
                out = get_from_frame(symb_frame, symb_val, TF_created_flag,
                                     GF_vars, TF_vars, LF_stack)
                if not out:
                    errprint('Attempted to read undefined variable!')
                    exit(55)
                check_var(symb_frame, symb_val, out.get_type(),
                          GF_vars, TF_vars, LF_stack)
                if out.get_type() == 'string':
                    print(parse_esc_seq(out.get_val()), end='')
                elif out.get_type() == None:
                    errprint(
                        'Attempted to read from uninitialized variable!')
                    exit(56)
                else:
                    print(out.get_val(), end='')
            case 'string':
                print(parse_esc_seq(symb_val), end='')
            case 'int' | 'bool' | 'nil':
                print(symb_val, end='')
