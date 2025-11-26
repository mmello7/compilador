int soma(int a, int b) {
    return a + b;
}

int main() {
    int x = 10;
    int resultado;

    resultado = soma(x, 5);

    if (resultado > 10) {
        x++;
    } else {
        x = 0;
    }

    return x;
}
