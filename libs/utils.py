import re
from libs.variable import variable


def parse_esc_seq(input: str) -> str:
    """
    Parse decadic escape sequences in IPPcode23 string
    """
    return re.sub(r'\\(\d{3})', lambda x: chr(int(x.group(1))), input)


def conv_to_correct(input: str, type: str) -> str | int:
    """
    Convert read input to correct data type
    """
    # add support for nil
    match type:
        case 'int':
            return int(input)
        case 'string':
            return str(input)
        # case 'bool':


def get_symb(symb_type: str, symb_val: str) -> list:
    match symb_type:
        case 'var':
            return get_var(symb_val)
        case 'string':
            return [str(symb_val), None, symb_type]
        case 'int':
            return [int(symb_val), None, symb_type]
        case 'bool':
            return [symb_val, None, symb_type]
        # TODO: add nil support


def get_var(var: str) -> list:
    """
    Get var id, frame and type from IPPcode23 format.

    Return a list with id, frame, type in this order.
    """
    return [var[3:], var[:2], 'var']


def get_from_stack(stack: list, query: str) -> dict:
    """
    Find var in topmost frame in stack
    """
    tmp = stack.pop()
    ret = tmp.get(query)
    stack.append(tmp)
    return ret


def update_on_stack(stack: list, query: str, val: variable):
    tmp = stack.pop()
    tmp.update({query: val})
    stack.append(tmp)


def get_from_frame(frame: str, query: str, GF: dict, TF: dict, LF: list):
    match frame:
        case 'GF':
            return GF.get(query)
        case 'TF':
            return TF.get(query)
        case 'LF':
            return get_from_stack(LF, query)
