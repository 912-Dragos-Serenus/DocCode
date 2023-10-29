from abc import ABC, abstractmethod

from super_hash_map.map import SuperHashMap
from .token import Token
from .lexical_error import LexicalError


class Pif(ABC):
    _SYMBOL_INDEX = -1
    _CONSTANT_INDEX = -2

    def __init__(self, tokens: list[Token]):
        self._program = []
        self._symbols = SuperHashMap()
        self._constants = SuperHashMap()
        self._tokens = tokens[:]

    @abstractmethod
    def remove_comments(self, code: str) -> str:
        pass

    @abstractmethod
    def add_constant(self, code: str) -> (bool, str):
        pass

    @abstractmethod
    def add_symbol(self, code: str) -> (bool, str):
        pass

    def analyse(self, filename: str) -> None:
        file = open(filename, "r", encoding='utf-8')
        code = file.read()
        file.close()

        code = self.remove_comments(code)

        while len(code) != 0:
            found = False
            for i in range(len(self._tokens)):
                if code.find(str(self._tokens[i])) == 0:
                    code = self.add(i, code)
                    found = True
                    break
            if not found:
                success, code = self.add_constant(code)
                if success:
                    continue
                success, code = self.add_symbol(code)
                if success:
                    continue
                raise LexicalError(code)

    def add(self, token_index: int, code: str) -> str:
        self._program.append((token_index, -1))

        token = self._tokens[token_index]
        code = code[len(str(token)):]

        return code
