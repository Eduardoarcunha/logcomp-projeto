class SymbolTable:
    def __init__(self) -> None:
        self.table = {}
        self.func_table = {}

    def create(self, symbol, type, value=None, var_type=None):
        if symbol in self.table.keys() or (var_type is not None and type != var_type):
            raise Exception
        self.table[symbol] = {"value": value, "type": type}

    def get(self, symbol):
        if symbol in self.table.keys():
            return self.table[symbol]
        raise Exception

    def set(self, symbol, value, var_type):
        if symbol in self.table.keys() and self.table[symbol]["type"] == var_type:
            self.table[symbol]["value"] = value
            return
        raise Exception

    def create_func(self, symbol, node, type):
        if symbol in self.func_table.keys():
            raise Exception
        self.func_table[symbol] = {"node": node, "type": type}

    def get_func(self, symbol):
        if symbol in self.func_table.keys():
            return self.func_table[symbol]
        raise Exception
