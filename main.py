from lexer.lexical_code_scanner import LexicalCodeScanner

if __name__ == "__main__":
    codigo = """
char endlessString[] = "This string never ends...
 float pi = 3,14;
 float piCorrect = 3.14;
    """
    sc = LexicalCodeScanner(codigo)
    sc.scan_all()
    sc.print_tokens()
    sc.print_symbol_table(sort_by_name=False)