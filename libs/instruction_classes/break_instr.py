"""
Author: Matúš Ďurica (xduric06)
"""


from ..instruction import Instruction
from ..utils import *
import sys


class Break(Instruction):
    def __init__(self, order):
        super().__init__(order, 'MOVE')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, TF_created_flag: int, args, processed_instr, stack, ds):
        self.check_num_of_args()
        print(
            '##################### INTERPRET DEBUG INFO #####################', file=sys.stderr)
        print('Instructions total: ', len(
            instructions), file=sys.stderr)
        print('Currently processed instruction: ',
              processed_instr.get_order(), file=sys.stderr)
        print('Processed instructions: ',
              processed_instr.get_order()-1, file=sys.stderr)
        print('Remaining instructions: ', len(
              instructions) - processed_instr.get_order(), file=sys.stderr)
        print('Variables in Global Frame: ', file=sys.stderr)
        for var in GF_vars:
            print(var, file=sys.stderr, end=', ')
        print('', file=sys.stderr)
        print('Variables in Temporary Frame: ', file=sys.stderr)
        for var in TF_vars:
            print(var, file=sys.stderr, end=', ')
        print('', file=sys.stderr)
        print('Variables in topmost Local Frame: ', file=sys.stderr)
        frame = LF_stack.pop()
        for var in frame:
            print(var, file=sys.stderr, end=', ')
        print('', file=sys.stderr)
        print(
            '################################################################', file=sys.stderr)
