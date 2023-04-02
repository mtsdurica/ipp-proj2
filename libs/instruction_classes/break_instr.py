from ..instruction import Instruction
from ..utils import *
import sys


class Break(Instruction):
    def __init__(self, order):
        super().__init__(order, 'MOVE')

    def execute(self, GF_vars: dict, TF_vars: dict, LF_stack: list, instructions: list, labels: dict, input_file_flag: int, args, processed_instr):
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
        print('Variables in Local Frame: ', file=sys.stderr)
        # TODO: redo
        # iterator = 0
        # for frame in LF_stack:
        #    iterator += 1
        #    if iterator == 1 and len(LF_stack) != 1:
        #        print('Function scope variables: ', file=sys.stderr)
        #    elif len(LF_stack) == 1 and iterator == 1:
        #        print('Main variables: ', file=sys.stderr)
        #    for var in frame:
        #        print(var, file=sys.stderr, end=', ')
        # print('', file=sys.stderr)
        print(
            '################################################################', file=sys.stderr)
