import sys
import argparse as ap
import xml.etree.ElementTree as ET
from libs.utils import *
from libs.factory import Factory


if __name__ == '__main__':
    GF_vars = {}
    TF_vars = {}
    instructions = []
    LF_stack = []
    labels = {}
    call_stack = []
    data_stack = []

    arg_parser = ap.ArgumentParser(
        prog='interpret', description='Interpretting XML file')
    arg_parser.add_argument('--source', metavar='file',
                            nargs='?', help='XML source file')
    arg_parser.add_argument('--input', metavar='file',
                            nargs='?', help='Input file')

    input_file_flag = 0
    TF_created_flag = 0
    args = arg_parser.parse_args()

    if not args.source and not args.input:
        # add correct error code
        exit('Zabudol si subor ty gazda')

    if args.input:
        input_file_flag = 1
        args.input = open(args.input)

    # parsing XML
    if args.source:
        try:
            tree = ET.parse(args.source)
        except ET.ParseError:
            errprint('Badly formatted XML file!')
            exit(31)

    else:
        tree = ET.parse(sys.stdin)

    program = tree.getroot()

    for node in program:
        if not re.match(r'^instruction$', node.tag):
            errprint('Bad node tag!')
            exit(32)
        opcode = node.attrib.get('opcode', 'ERR:NotFound')
        if opcode == 'ERR:NotFound':
            errprint('Missing opcode!')
            exit(32)
        try:
            try:
                order = int(node.attrib.get('order'))
            except ValueError:
                errprint('Number as order!')
                exit(32)
        except TypeError:
            errprint('Missing order!')
            exit(32)
        instr = Factory.create(opcode, order)
        instructions.append(instr)

        for arg in node:
            if re.match(r'^arg[\d]+$', arg.tag):
                if arg.attrib.get('type') == 'string':
                    if not arg.text:
                        arg_text = ''
                    else:
                        arg_text = parse_esc_seq(str(arg.text))
                else:
                    arg_text = arg.text
                instr.add_arg(arg.attrib.get('type'),
                              arg_text, arg.tag)
            else:
                errprint('Bad argument tag!')
                exit(32)
        for index, checked in enumerate(instr.get_args()):
            if int(checked.get_order()) != index+1:
                errprint('Bad argument order!')
                exit(32)

    instructions = sorted(instructions, key=lambda x: x.get_order())
    ind = 1
    last = 0
    for i in instructions:
        if i.get_order() == last:
            errprint('Duplicit order!')
            exit(32)
        i.set_order(ind)
        last = i.get_order()
        ind += 1

    iterator_obj = iter(instructions)
    # print(instructions[0])
    while True:
        try:
            current_instruction = next(iterator_obj)
        except StopIteration:
            break
        # print(current_instruction.get_opcode(),
        #      current_instruction.get_order())
        tmp = iterator_obj

        if current_instruction.get_opcode() == 'JUMP' or current_instruction.get_opcode() == 'JUMPIFNEQ' or current_instruction.get_opcode() == 'JUMPIFEQ' or current_instruction.get_opcode() == 'CALL' or current_instruction.get_opcode() == 'RETURN':
            iterator_obj = current_instruction.execute(GF_vars, TF_vars, LF_stack, instructions,
                                                       labels, input_file_flag, TF_created_flag, args, current_instruction, call_stack, data_stack)
            if not iterator_obj:
                iterator_obj = tmp
                # print('ahoj')
        elif current_instruction.get_opcode() == 'CREATEFRAME' or current_instruction.get_opcode() == 'PUSHFRAME':
            TF_created_flag = current_instruction.execute(GF_vars, TF_vars, LF_stack, instructions,
                                                          labels, input_file_flag, TF_created_flag, args, current_instruction, call_stack, data_stack)
        else:
            current_instruction.execute(GF_vars, TF_vars, LF_stack, instructions,
                                        labels, input_file_flag, TF_created_flag, args, current_instruction, call_stack, data_stack)
