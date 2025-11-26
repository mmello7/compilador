int main() {
    int x = 10;
    float y;
    
    y = calcula(x, 5); // Teste de chamada de função
    
    // Erro Léxico: '@' é um caractere ilegal
    int z = x @ 2; 
    
    // Erro Sintático: Falta um ';' no final da linha
    return y
}