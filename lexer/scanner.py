from lexer.operators import OPERATORS_2, OPERATORS_1, DELIMS
from lexer.keywords import KEYWORDS
from lexer.token import TokenType, Token
from typing import List, Dict
from lexer.operators import DELIMS, OPERATORS_1, OPERATORS_2
import pdb



class Scanner:
    def __init__(self, text: str):
        self.text = text
        self.i = 0                     # índice atual no código

    # olhar caractere atual sem consumir
    def _peek(self) -> str:
        return self.text[self.i] if self.i < len(self.text) else "\0"

    # olhar dois caracteres (para operadores de 2 chars)
    def _peek2(self) -> str:
        if self.i + 1 < len(self.text):
            return self.text[self.i] + self.text[self.i + 1]
        return "\0\0"

    # avança e retorna caractere atual
    def _advance(self) -> str:
        ch = self._peek()
        self.i += 1
        return ch