import sys
import argparse as ap
import xml.etree.ElementTree as ET
from libs.instruction import Instruction
from libs.variable import Variable
from libs.utils import *
from libs.factory import Factory


if __name__ == '__main__':
    GF_vars = {}
    TF_vars = {}
    instructions = []
    LF_stack = []
    labels = {}

    arg_parser = ap.ArgumentParser(
        prog='interpret', description='Interpretting XML file')
    arg_parser.add_argument('--source', metavar='file',
                            nargs='?', help='XML source file')
    arg_parser.add_argument('--input', metavar='file',
                            nargs='?', help='Input file')

    input_file_flag = 0

    args = arg_parser.parse_args()

    if not args.source and not args.input:
        # add correct error code
        exit('Zabudol si subor ty gazda')

    if args.input:
        input_file_flag = 1

    # parsing XML
    if args.source:
        tree = ET.parse(args.source)
    else:
        tree = ET.parse(sys.stdin)

    program = tree.getroot()

    for node in program:
        instr = Factory.create(node.attrib.get('opcode'),
                               int(node.attrib.get('order')))
        if not instructions:
            instructions.append(instr)
        else:
            if (
                instructions[-1].get_order() != instr.get_order()
                and (instr.get_order() - instructions[-1].get_order()) == 1
            ):
                instructions.append(instr)
            else:
                print('Error: Bad instruction order', file=sys.stderr)
                exit(32)

        for arg in node:
            instr.add_arg(arg.attrib.get('type'), arg.text.strip())

    iterator_obj = iter(instructions)
    while True:
        try:
            current_instruction = next(iterator_obj)
        except StopIteration:
            break

        tmp = iterator_obj

        if current_instruction.get_opcode() == 'JUMP' or current_instruction.get_opcode() == 'JUMPIFNEQ' or current_instruction.get_opcode() == 'JUMPIFEQ':
            iterator_obj = current_instruction.execute(GF_vars, TF_vars, LF_stack, instructions,
                                                       labels, input_file_flag, args, current_instruction)
            if not iterator_obj:
                iterator_obj = tmp
        else:
            current_instruction.execute(GF_vars, TF_vars, LF_stack, instructions,
                                        labels, input_file_flag, args, current_instruction)
