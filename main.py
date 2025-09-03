from lexer.scanner import Scanner

if __name__ == "__main__":
    codigo = """
    #include <std.io>
    #include <string.h>
    int a = 10;
    int b = 30;
    // kkkkkkk jorge vitor comentarios
    if (a >= 10)  // oi isso nao é pra quebrar
        a = b + 5;
    }
    #ifdef
    /* 
        oi nao eh pra quebrar
    oie*/
    int a
    char greetings[] = "Hello World!";
    char gorgonzola = "q";
    float pi = 3.14;
    int dez = 10;
    """
    sc = Scanner(codigo)
    sc.scan_all()
    sc.print_tokens()
    sc.print_symbol_table(sort_by_name=False)