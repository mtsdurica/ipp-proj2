import sys
import argparse as ap
import re
import xml.etree.ElementTree as ET
from libs.instruction import instruction
from libs.variable import variable
from libs.utils import *


GF_vars = {}
TF_vars = {}
instructions = []
LF_stack = []
instr_stack = {}


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

for i in program:
    instr = instruction(int(i.attrib.get('order')), i.attrib.get('opcode'))
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

    for a in i:
        instr.add_arg(a.attrib.get('type'), a.text.strip())
        args_list = instr.get_args()

iterator = iter(instructions)
while True:
    try:
        i = next(iterator)
    except StopIteration:
        break
    # print(i.get_opcode(), file=sys.stderr)
    args_list = i.get_args()
    order = i.get_order()
    match i.get_opcode():
        # case 'NOT':
        # case 'TYPE':
        # case 'INT2CHAR':
        # case 'STRLEN':
        case 'MOVE':
            var_id, var_frame, var_type = get_var(args_list[0].get_val())
            symb_val, symb_frame, symb_type = get_symb(
                args_list[1].get_type(), args_list[1].get_val()
            )
            match var_frame:
                case 'GF':
                    if not symb_frame:
                        updated = GF_vars.get(var_id)
                        updated.set_val(symb_val)
                        updated.set_type(symb_type)
                    else:
                        updated = get_from_frame(
                            symb_frame, symb_val, GF_vars, TF_vars, LF_stack
                        )
                    GF_vars.update({var_id: updated})
                case 'LF':
                    if not symb_frame:
                        updated = get_from_stack(LF_stack, var_id)
                        updated.set_val(symb_val)
                        updated.set_type(symb_type)
                    else:
                        updated = get_from_frame(
                            symb_frame, symb_val, GF_vars, TF_vars, LF_stack
                        )
                    update_on_stack(LF_stack, var_id, updated)
                case 'TF':
                    if not symb_frame:
                        updated = TF_vars.get(var_id)
                        updated.set_val(symb_val)
                        updated.set_type(symb_type)
                    else:
                        updated = get_from_frame(
                            symb_frame, symb_val, GF_vars, TF_vars, LF_stack
                        )
                    TF_vars.update({var_id: updated})
            ###################
        case 'CREATEFRAME':
            TF_vars.clear()
        case 'PUSHFRAME':
            LF_stack.append(TF_vars.copy())
        case 'POPFRAME':
            TF_vars.clear()
            TF_vars = LF_stack.pop()
        # case 'RETURN':
        case 'BREAK':
            print(
                '##################### INTERPRET DEBUG INFO #####################', file=sys.stderr)
            print('Instructions total: ', len(instructions), file=sys.stderr)
            print('Currently processed instruction: ',
                  i.get_order(), file=sys.stderr)
            print('Processed instructions: ', i.get_order()-1, file=sys.stderr)
            print('Remaining instructions: ', len(
                instructions) - i.get_order(), file=sys.stderr)
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
        #####################
        # case 'POPS':
        case 'DEFVAR':
            var_id, var_frame, var_type = get_var(args_list[0].get_val())
            var_obj = variable(var_id)
            match var_frame:
                case 'GF':
                    GF_vars.update({var_obj.get_id(): var_obj})
                case 'TF':
                    TF_vars.update({var_obj.get_id(): var_obj})
                case 'LF':
                    update_on_stack(LF_stack, var_obj.get_id(), var_obj)
        # case 'PUSHS':
        case 'DPRINT':
            # TODO: rest of cases
            symb_val, symb_frame, symb_type = get_symb(
                args_list[0].get_type(), args_list[0].get_val())
            match symb_type:
                case 'var':
                    match symb_frame:
                        case 'GF':
                            out = GF_vars.get(symb_val)
                            if out.get_type() == 'string':
                                print(parse_esc_seq(out.get_val()),
                                      end='', file=sys.stderr)
                            else:
                                print(out.get_val(), end='', file=sys.stderr)
        case 'EXIT':
            symb_val, _, symb_type = get_symb(
                args_list[0].get_type(), args_list[0].get_val())
            if symb_type == 'int' and symb_val >= 0 and symb_val <= 49:
                exit(symb_val)
            else:
                exit(57)
        case 'WRITE':
            symb_val, symb_frame, symb_type = get_symb(
                args_list[0].get_type(), args_list[0].get_val()
            )
            match symb_type:
                case 'var':
                    match symb_frame:
                        case 'GF':
                            tmp = GF_vars.get(symb_val)
                            if tmp.get_type() == 'string':
                                print(parse_esc_seq(tmp.get_val()), end='')
                            else:
                                print(tmp.get_val(), end='')
                        case 'TF':
                            tmp = TF_vars.get(symb_val)
                            if tmp.get_type() == 'string':
                                print(parse_esc_seq(tmp.get_val()), end='')
                            else:
                                print(tmp.get_val(), end='')
                        case 'LF':
                            tmp = get_from_stack(LF_stack, symb_val)
                            if tmp.get_type() == 'string':
                                print(parse_esc_seq(tmp.get_val()), end='')
                            else:
                                print(tmp.get_val(), end='')
                case 'bool':
                    print(symb_val, end='')
                case 'string':
                    print(parse_esc_seq(symb_val), end='')
                case 'int':
                    print(symb_val, end='')
                case 'nil':
                    # TODO: add nil support
                    pass
        case 'LABEL':
            lb_id = args_list[0].get_val()
            lb_order = i.get_order()
            instr_stack.update({lb_id: lb_order})
        case 'JUMP':
            lb_id = args_list[0].get_val()
            lb_order = i.get_order()
            if instr_stack.get(lb_id, 'NotFound') == 'NotFound':
                found_label = ''
                for sub in instructions[lb_order:]:
                    sub_val = sub.get_args()[0].get_val()
                    sub_opcode = sub.get_opcode()
                    if sub_val == lb_id and sub_opcode == 'LABEL':
                        found_label = sub_val
                        found_order = sub.get_order()
                        break
                if not found_label:
                    # TODO: proper error handling
                    exit('solim')
                else:
                    instr_stack.update({found_label: found_order})
            label = instr_stack.get(lb_id)
            iterator = iter(instructions[label-1:])
        # case 'CALL':
        #############################
        case 'JUMPIFEQ':
            lb_id = args_list[0].get_val()
            lb_order = i.get_order()
            symb1_val, symb1_frame, symb1_type = get_symb(
                args_list[1].get_type(), args_list[1].get_val())
            symb2_val, symb2_frame, symb2_type = get_symb(
                args_list[2].get_type(), args_list[2].get_val())
            # TODO: add null
            if symb1_type != symb2_type:
                exit(53)
            if symb1_val == symb2_val:
                if instr_stack.get(lb_id, 'NotFound') == 'NotFound':
                    found_label = ''
                    for sub in instructions[lb_order:]:
                        sub_val = sub.get_args()[0].get_val()
                        sub_opcode = sub.get_opcode()
                        if sub_val == lb_id and sub_opcode == 'LABEL':
                            found_label = sub_val
                            found_order = sub.get_order()
                            break
                    if not found_label:
                        # TODO: proper error handling
                        exit('solim')
                    else:
                        instr_stack.update({found_label: found_order})
                label = instr_stack.get(lb_id)
                iterator = iter(instructions[label-1:])
        case 'JUMPIFNEQ':
            lb_id = args_list[0].get_val()
            lb_order = i.get_order()
            symb1_val, symb1_frame, symb1_type = get_symb(
                args_list[1].get_type(), args_list[1].get_val())
            symb2_val, symb2_frame, symb2_type = get_symb(
                args_list[2].get_type(), args_list[2].get_val())
            # TODO: add null

            if GF_vars.get(symb1_val).get_val() != symb2_val:
                if instr_stack.get(lb_id, 'NotFound') == 'NotFound':
                    found_label = ''
                    for sub in instructions[lb_order:]:
                        sub_val = sub.get_args()[0].get_val()
                        sub_opcode = sub.get_opcode()
                        if sub_val == lb_id and sub_opcode == 'LABEL':
                            found_label = sub_val
                            found_order = sub.get_order()
                            break
                    if not found_label:
                        # TODO: proper error handling
                        exit('solim')
                    else:
                        instr_stack.update({found_label: found_order})
                label = instr_stack.get(lb_id)
                iterator = iter(instructions[label-1:])
        ######################
        case 'READ':
            var_id, var_frame, var_type = get_var(args_list[0].get_val())
            type = args_list[1].get_val()
            match var_frame:
                case 'GF':
                    if not input_file_flag:
                        line = input()
                    else:
                        with open(args.input) as f:
                            line = f.readline().rstrip()
                    tmp = GF_vars.get(var_id)
                    tmp.set_val(conv_to_correct(line, type))
                    tmp.set_type(type)
                    GF_vars.update({var_id: tmp})
                case 'TF':
                    if not input_file_flag:
                        line = input()
                    else:
                        with open(args.input) as f:
                            line = f.readline().rstrip()
                    tmp = TF_vars.get(var_id)
                    tmp.set_val(conv_to_correct(line, type))
                    tmp.set_type(type)
                    TF_vars.update({var_id: tmp})
                case 'LF':
                    if not input_file_flag:
                        line = input()
                    else:
                        with open(args.input) as f:
                            line = f.readline().rstrip()
                    tmp = get_from_stack(LF_stack, var_id)
                    tmp.set_val(conv_to_correct(line, type))
                    tmp.set_type(type)
                    update_on_stack(LF_stack, var_id, tmp)
    #################################
        case 'ADD':
            var_id, var_frame, var_type = get_var(args_list[0].get_val())
            symb1_val, symb1_frame, symb1_type = get_symb(
                args_list[1].get_type(), args_list[1].get_val())
            symb2_val, symb2_frame, symb2_type = get_symb(
                args_list[2].get_type(), args_list[2].get_val())

            if symb1_type == 'var' and symb2_type == 'int':
                tmp = GF_vars.get(symb1_val).get_val()
                sum = tmp + symb2_val
                updated = GF_vars.get(var_id)
                updated.set_val(sum)
                updated.set_type('int')
                GF_vars.update({var_id: updated})
        # case 'SUB':
        #    pass
        case 'MUL':
            pass
            # case 'EQ':
            # case 'LT':
            # case 'GT':
            # case 'AND':
            # case 'STRI2INT':
            # case 'CONCAT':
            # case 'GETCHAR':
            # case 'SETCHAR':
            # case 'OR':
        case 'IDIV':
            pass
