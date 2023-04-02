class Argument:
    def __init__(self, arg_type, arg_val):
        self._type = arg_type
        self._val = arg_val

    def get_type(self) -> str:
        return self._type

    def get_val(self) -> str | int:
        return self._val
