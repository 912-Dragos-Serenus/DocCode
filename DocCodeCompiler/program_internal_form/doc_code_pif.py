import re

from .pif import Pif
from .lexical_error import LexicalError
from .token import Token
from super_hash_map.map import SuperHashMap


class DocCodePif(Pif):
    def __init__(self, tokens_filename: str):
        file = open(tokens_filename, 'r', encoding='utf-8')
        lines = file.readlines()
        file.close()

        super().__init__([Token(line[:-1].replace("\\n", "\n")) for line in lines])

    def __add_others_helper(self, match: str, code: str, collection: SuperHashMap, index: int) -> (bool, str):
        if len(match) == 0:
            return False, code

        element = collection.get(match)
        if element is None:
            collection.put(match, collection.current_value)
            collection.current_value += 1
            element = collection.get(match)

        self._program.append((index, element.value))

        code = code[len(match):]
        return True, code

    @staticmethod
    def is_small_letter(letter: str) -> bool:
        if letter == 'ă':
            return True
        if letter == 'î':
            return True
        if letter == 'â':
            return True
        if letter == 'ș':
            return True
        if letter == 'ț':
            return True
        if not letter.isalpha():
            return False
        if letter.islower():
            return True
        return False

    @staticmethod
    def is_big_letter(letter: str) -> bool:
        if letter == 'Ă':
            return True
        if letter == 'Î':
            return True
        if letter == 'Â':
            return True
        if letter == 'Ș':
            return True
        if letter == 'Ț':
            return True
        if not letter.isalpha():
            return False
        if letter.isupper():
            return True
        return False

    def add_symbol(self, code: str) -> (bool, str):
        if not DocCodePif.is_big_letter(code[0]):
            return False, code

        match = code[0]
        valid = True
        index = 1
        state = 2  # 0 for letter, 1 for space
        while valid:
            if DocCodePif.is_small_letter(code[index]) or DocCodePif.is_big_letter(code[index]):
                match += code[index]
                state = 0
            else:
                if state == 0:
                    if code[index] == ' ':
                        match += code[index]
                        state = 1
                    else:
                        valid = False
                elif state == 1:
                    valid = False
            index += 1

        return self.__add_others_helper(match, code, self._symbols, self._SYMBOL_INDEX)

    def add_constant(self, code: str) -> (bool, str):
        if code[:8] != 'numărul ':
            return False, code

        if not code[8].isdigit():
            return False, code

        [_, nr, _] = code.split(' ')
        try:
            float(nr)
            match = 'numărul ' + nr
            return self.__add_others_helper(match, code, self._constants, self._CONSTANT_INDEX)
        except ValueError:
            return False, code

    @staticmethod
    def _special_point_split(text: str) -> list[str]:
        cnt = 0
        result = []
        current_part = ''
        for character in text:
            if character == '„':
                cnt += 1
            elif character == '”':
                cnt -= 1
            elif character == '.':
                if cnt > 0:
                    continue
                result.append(current_part)
                current_part = ''
            else:
                current_part += character
        result.append(current_part)
        return result

    def remove_comments(self, code: str) -> str:
        parts = code.split('\n\n\n\n')
        if len(parts) > 2:
            raise LexicalError(parts[2])
        if len(parts) < 2:
            raise LexicalError(code)

        new_code = parts[0] + "\n\n\n\n"
        body = parts[1]
        chapters = body.split("\n\n\n")
        if len(chapters) < 1:
            raise LexicalError(parts[0])

        main = chapters[0]
        chapters = chapters[1:]

        statements = self._special_point_split(main)[:-1]
        if_start = 1
        for statement in statements:
            if if_start > 0:
                new_code += statement + '.'
                if_start -= 1
                continue
            [_, instructions] = statement.split(',', 1)
            if instructions.find("verificăm dacă") != -1:
                if_start = 2
            new_code += ',' + instructions + '.'

        for chapter in chapters:
            [title, body] = chapter.split("\n\n", 1)
            new_code += "\n\n\n" + title + "\n\n"

            statements = self._special_point_split(body)[:-1]
            if_start = 1
            for statement in statements:
                if if_start > 0:
                    new_code += statement + '.'
                    if_start -= 1
                    continue
                [_, instructions] = statement.split(',', 1)
                if instructions.find("verificăm dacă") != -1:
                    if_start = 2
                new_code += ',' + instructions + '.'

        return new_code
