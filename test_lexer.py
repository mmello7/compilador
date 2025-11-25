from src.lexer import lexer

# Código C de exemplo
data = '''
int main() {
    int x = 10;
    float y = 3.14;
    char c = 'A';
    x += 5;
    if (x > 10) {
        y = y - 1.0;
    } else {
        y = y + 2.0;
    }
    return 0;
}
'''

# Passa o código para o lexer
lexer.input(data)

# Itera sobre os tokens
for tok in lexer:
    print(tok)
