from ..instruction import Instruction
from ..utils import *


class Label(Instruction):
    def __init__(self, order):
        super().__init__(order, 'LABEL')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        label_id = self.get_args()[0].get_val()
        label_order = self.get_order()
        if labels.get(label_id):
            exit(52)
        labels.update({label_id: label_order})
