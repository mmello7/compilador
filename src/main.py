import sys
import json

from lexer import lexer, lex_error, symbol_table
from parser import parser, parse_error

def main():
    if len(sys.argv) != 2:
        print("Como usar: python main.py <caminho_para_o_arquivo.c>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
         with open(file_path, 'r') as f:
              code = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        sys.exit(1)
        
    ast = parser.parse(code, lexer=lexer)

    print(f"DIAGNÓSTICO: A lista lex_error tem {len(lex_error)} erros.")
    print(f"DIAGNÓSTICO: A lista parse_error tem {len(parse_error)} erros.")

    has_errors = lex_error or parse_error

    if has_errors: 
        print("="*20 + "ERROS DE COMPILAÇÃO" + "="*20)
        
        if lex_error:
            print("\n --- Erros Léxicos ---")
            for err in lex_error:
                print(f"Linha {err['line']} : {err['column']} -> {err['type']}: '{err['value']}")

        if parse_error:
            print("\n--- Erros Sintáticos ---")
            for err in parse_error:
                print(f"Linha {err['line']}:{err['column']} -> {err['message']}")
                print("\n" + "="*58)
                print("A compilação falhou devido aos erros acima.")
                sys.exit(1)

    else:
        print("="*20 + " ANÁLISE CONCLUÍDA COM SUCESSO " + "="*20)
        print("\nNenhum erro léxico ou sintático encontrado.")
        print("\n--- Árvore Sintática Abstrata (AST) Gerada ---")
            
        print(json.dumps(ast, indent=2))
        print("\n" + "="*66)
        print("DIAGNÓSTICO: O programa acha que não há erros e vai tentar imprimir a AST.")
    
    print("\n--- Tabela de Símbolos ---")
    
    print(f"{'ORDEM' :<10} {'NOME DO SÍMBOLO'}")
    print("-" *30)

    sorted_symbols = sorted(symbol_table)

    for i, symbol in enumerate(sorted_symbols, 1):
        print(f"#{i:<9} {symbol}")

    
    print("\n" + "="*66)

if __name__ == '__main__':
    main()