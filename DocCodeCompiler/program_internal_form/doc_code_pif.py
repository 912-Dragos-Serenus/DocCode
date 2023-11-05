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
        state = 0  # 0 for big letter, 1 for small letter, 2 for space
        while valid:
            if state == 0:
                if self.is_small_letter(code[index]):
                    match += code[index]
                    state = 1
                elif code[index] == ' ':
                    match += code[index]
                    state = 2
                else:
                    valid = False
            elif state == 1:
                if self.is_small_letter(code[index]):
                    match += code[index]
                elif code[index] == ' ':
                    match += code[index]
                    state = 2
                else:
                    valid = False
            else:
                if self.is_big_letter(code[index]):
                    match += code[index]
                    state = 0
                else:
                    valid = False
            index += 1

        return self.__add_others_helper(match, code, self._symbols, self._SYMBOL_INDEX)

    def add_number_constant(self, code: str) -> (bool, str):
        if code[:8] != 'numărul ':
            return False, code

        if not code[8].isdigit():
            return False, code

        match = re.match(r'\d+', code[8:])
        if match:
            nr = match.group(0)
        else:
            return False, code
        try:
            float(nr)
            match = 'numărul ' + nr
            return self.__add_others_helper(match, code, self._constants, self._CONSTANT_INDEX)
        except ValueError:
            return False, code

    def add_string_constant(self, code: str) -> (bool, str):
        if code[0] != '„':
            return False, code

        index = code.find('”')
        if index == -1:
            raise LexicalError("Invalid string constant")

        return self.__add_others_helper(code[0: index + 1], code, self._constants, self._CONSTANT_INDEX)

    def add_constant(self, code: str) -> (bool, str):
        res = self.add_number_constant(code)
        return res if res[0] else self.add_string_constant(code)

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

            if character == '.' and cnt == 0:
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
