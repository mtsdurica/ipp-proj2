from .instruction_classes.add import Add
from .instruction_classes.break_instr import Break
from .instruction_classes.createframe import Createframe
from .instruction_classes.defvar import Defvar
from .instruction_classes.dprint import Dprint
from .instruction_classes.exit import Exit
from .instruction_classes.idiv import Idiv
from .instruction_classes.jump import Jump
from .instruction_classes.jumpifeq import Jumpifeq
from .instruction_classes.jumpifneq import Jumpifneq
from .instruction_classes.label import Label
from .instruction_classes.move import Move
from .instruction_classes.mul import Mul
from .instruction_classes.popframe import Popframe
from .instruction_classes.pushframe import Pushframe
from .instruction_classes.read import Read
from .instruction_classes.sub import Sub
from .instruction_classes.write import Write
from .instruction_classes.call import Call
from .instruction_classes.return_instr import Return
from .instruction_classes.lt import Lt
from .instruction_classes.gt import Gt
from .instruction_classes.eq import Eq
from .instruction_classes.pushs import Pushs
from .instruction_classes.pops import Pops
from .instruction_classes.type import Type
from .instruction_classes.int2char import Int2char
from .instruction_classes.stri2int import Stri2int
from .instruction_classes.concat import Concat
from .instruction_classes.strlen import Strlen
from .instruction_classes.getchar import Getchar
from .instruction_classes.setchar import Setchar
from .instruction_classes.or_instr import Or
from .instruction_classes.and_instr import And
from .instruction_classes.not_instr import Not
from .utils import *


class Factory:
    @classmethod
    def create(cls, opcode: str, order: int):
        if not re.match(r'^\d+$', str(order)):
            errprint('Bad order!')
            exit(32)
        match opcode.upper():
            case 'NOT':
                return Not(order)
            case 'TYPE':
                return Type(order)
            case 'INT2CHAR':
                return Int2char(order)
            case 'STRLEN':
                return Strlen(order)
            case 'MOVE':
                return Move(order)
            case 'CREATEFRAME':
                return Createframe(order)
            case 'PUSHFRAME':
                return Pushframe(order)
            case 'POPFRAME':
                return Popframe(order)
            case 'RETURN':
                return Return(order)
            case 'BREAK':
                return Break(order)
            case 'POPS':
                return Pops(order)
            case 'DEFVAR':
                return Defvar(order)
            case 'PUSHS':
                return Pushs(order)
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
                return Call(order)
            case 'JUMPIFEQ':
                return Jumpifeq(order)
            case 'JUMPIFNEQ':
                return Jumpifneq(order)
            case 'READ':
                return Read(order)
            case 'ADD':
                return Add(order)
            case 'SUB':
                return Sub(order)
            case 'MUL':
                return Mul(order)
            case 'EQ':
                return Eq(order)
            case 'LT':
                return Lt(order)
            case 'GT':
                return Gt(order)
            case 'AND':
                return And(order)
            case 'STRI2INT':
                return Stri2int(order)
            case 'CONCAT':
                return Concat(order)
            case 'GETCHAR':
                return Getchar(order)
            case 'SETCHAR':
                return Setchar(order)
            case 'OR':
                return Or(order)
            case 'IDIV':
                return Idiv(order)
            case _:
                errprint('Unknown instruction!')
                exit(32)
