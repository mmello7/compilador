from src.lexer import lexer
from src.lexer import lex_error

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

print("=========TOKENS GERADOS=========")
# Itera sobre os tokens
for tok in lexer:
    print(tok)
#Imprimir os erros lexicos
print("\n===== ERROS LÉXICOS =====")
if len(lex_error) == 0:
    print("Nenhum erro léxico encontrado.")
else:
    for erro in lex_error:
        print(erro)

# limpar erros antes dos próximos testes
lex_error.clear()



# =====================================================
# A PARTIR DAQUI COMEÇAM OS TESTES EXIGIDOS PELO BAREMA
# =====================================================


# Função auxiliar para facilitar rodar vários testes
def testar(codigo, titulo):
    print("\n============================================")
    print(f"TESTE: {titulo}")
    print("============================================\n")

    lexer.input(codigo)

    print("TOKENS:")
    for tok in lexer:
        print(tok)

    print("\nERROS LÉXICOS:")
    if len(lex_error) == 0:
        print("Nenhum erro léxico encontrado.")
    else:
        for erro in lex_error:
            print(erro)

    lex_error.clear()  # Limpar para próximo teste



# 1) OPERADORES COMPOSTOS
testar("""
a += 1;
b -= 2;
c *= 3;
d /= 4;
e %= 5;
x <<= 2;
y >>= 3;
i++;
j--;
""", "Operadores Compostos")


# 2) FLOATS COMPLETOS (incluindo notação científica)
testar("""
float a = 10.5;
float b = .5;
float c = 2e10;
float d = 3.14e-2;
""", "Floats com Notação Científica")


# 3) CHAR VÁLIDOS
testar("""
char a = 'a';
char b = '\\n';
char c = '\\t';
char d = '\\\'';
char e = '\\"';
""", "Char com Escapes")


# 4) CHAR INVÁLIDO (erro)
testar("char x = 'a\n", "Char NÃO FECHADO")


# 5) STRINGS VÁLIDAS
testar("""
char* s1 = "Olá mundo";
char* s2 = "Escape \\n dentro";
char* s3 = "Aspas: \\"isso\\" aqui";
""", "Strings com Escapes")


# 6) STRING INVÁLIDA
testar("\"string sem fechar\n", "String NÃO FECHADA")


# 7) COMENTÁRIOS
testar("""
int x = 10; // comentário simples

/*
bloco
de
comentário
*/

float y = 3.14;
""", "Comentários de Linha e Bloco")

#desculpaaaaaaaaaakkkkkk eu cliquei p consertar, achei q era no meu dps q vi que era no test my bad kkkkkkkkkk de boa muie <3 
# 8) ERROS LÉXICOS GERAIS
testar("""
@
$
~
#
""", "Erros Léxicos Diversos")
#vei acho q agr abraça os erros que luis pediu no doc de barema
#ta completinho