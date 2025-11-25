// teste.c

int main() {
    int x = 10;
    int y;
    
    y = calcula(x, 5); // Teste de chamada de função
    
    if (y > 10) {
        y++; // Teste de pós-incremento
    }

    // Erros para testar o sistema de relatório
    float z = 10.5;
    int w = z @ 2; // Erro léxico (caractere ilegal '@')
    
    if (w > 5) // Erro sintático (falta o ';')
        return w
}
