from ..instruction import Instruction
from ..utils import *


class Createframe(Instruction):
    def __init__(self, order):
        super().__init__(order, 'CREATEFRAME')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
        TF_vars.clear()
