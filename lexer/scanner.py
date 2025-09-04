from lexer.operators import OPERATORS_2, OPERATORS_1, DELIMS
from lexer.keywords import KEYWORDS
from lexer.token import TokenType, Token
from typing import List, Dict
from lexer.operators import DELIMS, OPERATORS_1, OPERATORS_2

stack = []

class Scanner:
    def __init__(self, codigo: str):
        self.codigo = codigo
        self.i = 0                     # índice atual no código
        self.tokens: List[Token] = []  # lista de tokens encontrados
        self.symbols: Dict[str, int] = {}  # tabela de símbolos {nome: índice}
        self._next_sym_id = 1          # próximo id para identificadores (id1, id2...)

    # olhar caractere atual sem consumir
    def _peek(self) -> str:
        return self.codigo[self.i] if self.i < len(self.codigo) else "\0"

    # olhar dois caracteres (para operadores de 2 chars)
    def _peek2(self) -> str:
        if self.i + 1 < len(self.codigo):
            return self.codigo[self.i] + self.codigo[self.i + 1]
        return "\0\0"

    # avança e retorna caractere atual
    def _advance(self) -> str:
        ch = self._peek()
        self.i += 1
        return ch

    # regra: identificador começa com letra ou underscore
    @staticmethod
    def _is_ident_start(ch: str) -> bool:
        return ch.isalpha() or ch == "_"

    # regra: dentro do identificador pode ter letras, dígitos ou underscore
    @staticmethod
    def _is_ident_part(ch: str) -> bool:
        return ch.isalnum() or ch == "_"

    # emite um identificador (gera idN e atualiza tabela de símbolos)
    def _emit_id(self, name: str):
        if name not in self.symbols:
            self.symbols[name] = self._next_sym_id
            self._next_sym_id += 1
        sym_id = self.symbols[name]
        self.tokens.append(Token(TokenType.ID, f"id{sym_id}"))

    # função principal: percorre todo o código e gera lista de tokens
    def scan_all(self) -> List[Token]:
        while self.i < len(self.codigo):
            ch = self._peek()

            if ch == '"':
                lex = ""
                self.i += 1
                while True:
                    current = self._advance()
                    if current == '"' or current == "\0":
                        self.tokens.append(Token(TokenType.STR_VALUE, lex))
                        break

                    lex += current
                    
            # ignora espaços em branco
            if ch.isspace():
                self._advance()
                continue

            # Identificadores e palavras-chave
            if self._is_ident_start(ch):
                lex = self._advance()
                while self._is_ident_part(self._peek()):
                    lex += self._advance()
                if lex in KEYWORDS:
                    self.tokens.append(Token(TokenType.KEYWORD, lex))
                else:
                    self._emit_id(lex)
                continue

            # Números
            if ch.isdigit():
                lex = self._advance()
                while self._peek().isdigit():
                    lex += self._advance()
                # se após número vier letra/_ → erro único (ex: "8a")
                if self._is_ident_part(self._peek()):
                    while self._is_ident_part(self._peek()):
                        lex += self._advance()
                    self.tokens.append(Token(TokenType.ERRO, lex))
                else:
                    self.tokens.append(Token(TokenType.NUM, lex))
                continue

            isLineComment = self._peek2() == "//"
            if isLineComment:
                while True:
                    current = self._advance()
                    if current == "\n" or current == "\0":
                        break


            isMultilineComment = self._peek2() == "/*"
            if isMultilineComment:
                while True:
                    if self._peek2() == "*/":
                        self.i += 2
                        break

                    # edge case: comentário aberto e não fechado
                    if self._peek() == "\0":
                        break
                        
                    self.i += 1

            isPreprocessorDirective = self._peek() == "#"
            if isPreprocessorDirective:
                lex = ""
                while True:
                    current = self._advance()
                    if current == "\n" or current == "\0":
                        self.tokens.append(Token(TokenType.PP_DIRECTIVE, lex))
                        break

                    lex += current
        
            
            # Operadores (checa primeiro os de 2 chars)
            two = self._peek2()
            if two in OPERATORS_2:
                self.tokens.append(Token(OPERATORS_2[two], two))
                self.i += 2
                continue
            if ch in OPERATORS_1:
                self.tokens.append(Token(OPERATORS_1[ch], self._advance()))
                continue

            # Delimitadores
            PAIRS = {"(": ")", "[": "]", "{": "}"}
            if ch in DELIMS:
                if ch in PAIRS:
                    stack.append(ch)
                elif ch in PAIRS.values():
                    if not stack:
                        self.tokens.append(Token(TokenType.ERRO, self._advance()))
                    else:
                        stack.pop()
                
                self.tokens.append(Token(DELIMS[ch], self._advance()))               
                continue

            # Qualquer outro caractere é erro
            self.tokens.append(Token(TokenType.ERRO, self._advance()))

        # fim de arquivo
        self.tokens.append(Token(TokenType.EOF, ""))
        return self.tokens

    # impressão simples da lista de tokens
    def print_tokens(self):
        print("\n=== LISTA DE TOKENS ===")
        for t in self.tokens:
            print(f"{t.tipo.name:<7}  {t.lexema}")

    # impressão da tabela de símbolos
    def print_symbol_table(self, sort_by_name: bool = False):
        print("\n=== TABELA DE SÍMBOLOS ===")
        items = list(self.symbols.items())
        if sort_by_name:
            items.sort(key=lambda x: x[0])  # ordena alfabeticamente
        for name, idx in items:
            print(f"id{idx:<3}  {name}")