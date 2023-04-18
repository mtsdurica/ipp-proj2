from ..instruction import Instruction
"""
Author: Matúš Ďurica (xduric06)
"""


from ..utils import *


class Createframe(Instruction):
    def __init__(self, order):
        super().__init__(order, 'CREATEFRAME')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        TF_vars.clear()
        TF_created_flag = 1
        return TF_created_flag
