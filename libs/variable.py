class Variable:
    def __init__(self, id):
        self._id = id
        self._val = None
        self._type = None

    def set_type(self, type):
        self._type = type

    def set_val(self, val):
        self._val = val

    def get_id(self):
        return self._id

    def get_val(self):
        return self._val

    def get_type(self):
        return self._type
