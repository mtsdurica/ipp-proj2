"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *


class Pushframe(Instruction):
    def __init__(self, order):
        super().__init__(order, 'PUSHFRAME')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        if not TF_created_flag:
            errprint('Pushing of not existing TF attempted!')
            exit(55)
        LF_stack.append(TF_vars.copy())
        TF_vars.clear()
        TF_created_flag = 0
        return TF_created_flag
