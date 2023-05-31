"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *


class Label(Instruction):
    def __init__(self, order):
        super().__init__(order, 'LABEL')

    def check_num_of_args(self):
        if len(self._args) != 1:
            errprint('Undefined amount of arguments in instruction!')
            exit(32)

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        label_id = self.get_args()[0].get_val()
        label_order = self.get_order()
        if labels.get(label_id):
            errprint('Attempted redefinition of a label!')
            exit(52)
        labels.update({label_id: label_order})
