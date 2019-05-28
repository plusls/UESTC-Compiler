class SymbolTable(object):
    def __init__(self, symbol_list):
        self.__symbol_type = {}
        self.__idx = 0
        for s in symbol_list:
            self.add_type(s)

    def add_type(self, s):
        if s not in self.__symbol_type:
            self.__symbol_type[s] = self.__idx
            self.__idx += 1
    def get_type(self, s):
        if s not in self.__symbol_type:
            return None
        return self.__symbol_type[s]


symbol_list = ['begin', 'end', 'integer', 'if', 'then', 'else', 'function',
               'read', 'write', 10, 11, '=', '<>', '<=', '<', '>=',
               '>', '-', '*', ':=', '(', ')', ';']
type_table = SymbolTable(symbol_list)
