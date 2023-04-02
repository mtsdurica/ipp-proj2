from ..instruction import Instruction
from ..utils import *


class Pushframe(Instruction):
    def __init__(self, order):
        super().__init__(order, 'PUSHFRAME')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        LF_stack.append(TF_vars.copy())
