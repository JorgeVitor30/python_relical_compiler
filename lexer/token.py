# lexer/token.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

# ------------------------------
# Enum para tipos de tokens
# ------------------------------
class TokenType(Enum):
    # categorias gerais
    ID = auto()       # identificadores (variáveis, funções)
    KEYWORD = auto()  # palavras reservadas (int, if, while, etc.)
    NUM = auto()      # números inteiros
    EOF = auto()      # fim de arquivo
    ERRO = auto()     # sequência inválida (ex.: "8a")

    # operadores de 2 caracteres
    EQ = auto()       # ==
    NE = auto()       # !=
    LE = auto()       # <=
    GE = auto()       # >=

    # operadores de 1 caractere
    ASSIGN = auto()   # =
    PLUS = auto()     # +
    MINUS = auto()    # -
    STAR = auto()     # *
    SLASH = auto()    # /
    LT = auto()       # <
    GT = auto()       # >

    # delimitadores
    SEMI = auto()     # ;
    COMMA = auto()    # ,
    LPAREN = auto()   # (
    RPAREN = auto()   # )
    LBRACE = auto()   # {
    RBRACE = auto()   # }

# ------------------------------
# Classe Token
# ------------------------------
@dataclass
class Token:
    tipo: TokenType           # tipo do token (enum)
    lexema: str               # texto exato do código
    atributo: Optional[Any] = None  # opcional: valor convertido ou referência para tabela de símbolos

    def __repr__(self) -> str:
        if self.atributo is not None:
            return f"<{self.tipo.name}, {self.lexema}, {self.atributo}>"
        return f"<{self.tipo.name}, {self.lexema}>"
