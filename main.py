from lexer.scanner import Scanner

if __name__ == "__main__":
    codigo = """
    int a = 10;
    int b = 30;
    if (a >= 10) {
        a = b + 5;
    }
    int a
    """
    sc = Scanner(codigo)
    sc.scan_all()
    sc.print_tokens()
    sc.print_symbol_table(sort_by_name=False)