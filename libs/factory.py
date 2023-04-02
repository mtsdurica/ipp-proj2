from .instruction_classes.add import Add
from .instruction_classes.break_instr import Break
from .instruction_classes.createframe import Createframe
from .instruction_classes.defvar import Defvar
from .instruction_classes.dprint import Dprint
from .instruction_classes.exit import Exit
from .instruction_classes.jump import Jump
from .instruction_classes.jumpifeq import Jumpifeq
from .instruction_classes.jumpifneq import Jumpifneq
from .instruction_classes.label import Label
from .instruction_classes.move import Move
from .instruction_classes.popframe import Popframe
from .instruction_classes.pushframe import Pushframe
from .instruction_classes.read import Read
from .instruction_classes.write import Write


class Factory:
    @classmethod
    def create(cls, opcode: str, order: int):
        match opcode.upper():
            case 'NOT':
                pass
            case 'TYPE':
                pass
            case 'INT2CHAR':
                pass
            case 'STRLEN':
                pass
            case 'MOVE':
                return Move(order)
            case 'CREATEFRAME':
                return Createframe(order)
            case 'PUSHFRAME':
                return Pushframe(order)
            case 'POPFRAME':
                return Popframe(order)
            case 'RETURN':
                pass
            case 'BREAK':
                return Break(order)
            case 'POPS':
                pass
            case 'DEFVAR':
                return Defvar(order)
            case 'PUSHS':
                pass
            case 'DPRINT':
                return Dprint(order)
            case 'EXIT':
                return Exit(order)
            case 'WRITE':
                return Write(order)
            case 'LABEL':
                return Label(order)
            case 'JUMP':
                return Jump(order)
            case 'CALL':
                pass
            case 'JUMPIFEQ':
                return Jumpifeq(order)
            case 'JUMPIFNEQ':
                return Jumpifneq(order)
            case 'READ':
                return Read(order)
            case 'ADD':
                return Add(order)
            case 'SUB':
                pass
            case 'MUL':
                pass
            case 'EQ':
                pass
            case 'LT':
                pass
            case 'GT':
                pass
            case 'AND':
                pass
            case 'STRI2INT':
                pass
            case 'CONCAT':
                pass
            case 'GETCHAR':
                pass
            case 'SETCHAR':
                pass
            case 'OR':
                pass
            case 'IDIV':
                pass
