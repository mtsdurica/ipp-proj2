import re
import sys
from libs.variable import Variable


def parse_esc_seq(input: str) -> str:
    """
    Parse decadic escape sequences in IPPcode23 string
    """
    return re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), input)


def conv_to_correct(input: str, type: str) -> str | int:
    """
    Convert read input to correct data type
    """
    if not input:
        return 'nil'
    match type:
        case 'int':
            try:
                return int(input)
            except ValueError:
                return 'nil'
        case 'string':
            return str(input)
        case 'bool':
            if re.match(r'^true$', input, re.IGNORECASE):
                return 'true'
            else:
                return 'false'


def get_symb(symb_type: str, symb_val: str) -> list:
    """
    Get symbol value, frame and type from IPPcode23 format
    """
    match symb_type:
        case 'var':
            return get_var(symb_val)
        case 'string':
            return [str(symb_val), None, symb_type]
        case 'int':
            if re.match(r'^(\+|-)?\d+$', symb_val):
                return [int(symb_val), None, symb_type]
            else:
                errprint('Bad int format!')
                exit(32)
        case 'bool':
            return [symb_val, None, symb_type]
        case 'nil':
            return ['', None, symb_type]


def get_var(var: str) -> list:
    """
    Get var id, frame and type from IPPcode23 format.

    Return a list with id, frame, type in this order.
    """
    return [var[3:], var[:2].upper(), 'var']


def get_from_stack(stack: list, query: str) -> dict:
    """
    Find var in topmost frame on stack
    """
    popped = stack.pop()
    ret = popped.get(query)
    stack.append(popped)
    return ret


def check_var(frame: str, query: str, var_type: str, GF: dict, TF: dict, LF: list):
    """
    Check if var exists and check if var is initialized
    """
    # if var_type != None and var_type == 'var':
    #   exit(56)
    checked = get_from_frame(frame, query, GF, TF, LF)
    if not checked:
        exit(54)


def update_on_stack(stack: list, query: str, updated_obj: Variable):
    """
    Update var in topmost frame on stack
    """
    tmp = stack.pop()
    tmp.update({query: updated_obj})
    stack.append(tmp)


def get_from_frame(frame: str, query: str, GF: dict, TF: dict, LF: list):
    """
    Find var in frame
    """
    match frame:
        case 'GF':
            return GF.get(query)
        case 'TF':
            return TF.get(query)
        case 'LF':
            return get_from_stack(LF, query)


def update_in_frame(frame: str, query: str, updated_obj: Variable, GF: dict, TF: dict, LF: list):
    """
    Update var in frame
    """
    match frame:
        case 'GF':
            GF.update({query: updated_obj})
        case 'TF':
            TF.update({query: updated_obj})
        case 'LF':
            update_on_stack(LF, query, updated_obj)


def find_label(instructions: list, jump_label: str, jump_instr_order: int, labels: dict):
    """
    Find processed and unprocessed label
    """
    # trying to get label from labels dict,
    # if not found the rest of the instructions will be checked until it is found
    if jump_label not in labels:
        found_label = ''
        # searching in intructions list from the index of the jump instruction
        # no need to search from the first index, since that would mean the label is already in labels dict
        # and therefore would be found
        for checked in instructions:
            checked_opcode = checked.get_opcode()
            # mozno argumenty chekc
            if checked_opcode == 'LABEL':
                checked_val = checked.get_args()[0].get_val()
                if checked_val == jump_label:
                    found_label = checked_val
                    found_order = checked.get_order()
                    break
        if not found_label:
            # TODO: proper error handling
            errprint('Label not found!')
            exit(52)
        else:
            # updating labels dict with found label
            labels.update({found_label: found_order})
    return labels.get(jump_label)


def errprint(msg: str) -> None:
    print('ERROR: ' + msg, file=sys.stderr)
