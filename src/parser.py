import ply.yacc as yacc
from lexer import lexer, tokens, find_collum

parse_error = []

def p_program(p):
    '''program : external_declaration_list'''
    p[0] = p[1]


def p_external_declaration_list(p):
    '''external_declaration_list : external_declaration_list external_declaration
                                 | external_declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration'''
    p[0] = p[1]


def p_declaration(p):
    '''declaration : type_specifier init_declarator_list SEMI'''
    p[0] = ('declare', p[1], p[2])


def p_type_specifier(p):
    '''type_specifier : INT
                      | FLOAT
                      | DOUBLE
                      | CHAR
                      | VOID'''
    p[0] = p[1]


def p_init_declarator_list(p):
    '''init_declarator_list : init_declarator
                            | init_declarator_list COMMA init_declarator'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_init_declarator(p):
    '''init_declarator : ID
                       | ID ASSIGN constant'''
    if len(p) == 2:
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[3])


def p_constant(p):
    '''constant : NUMBER
                | FLOATNUM
                | CHAR_CONST
                | STRING'''
    p[0] = p[1]


def p_function_definition(p):
    '''function_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement
                           | type_specifier ID LPAREN RPAREN compound_statement'''
    
    if len(p) == 7: 
        p[0] = ('function', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('function', p[1], p[2], [], p[5])


def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter_list COMMA parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    '''parameter : type_specifier ID'''
    p[0] = (p[1], p[2])


def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE
                          | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []


def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    '''statement : declaration
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
                 | compound_statement'''
    p[0] = p[1]


def p_expression_statement(p):
    '''expression_statement : expression SEMI
                            | SEMI'''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = None


def p_expression(p):
    '''expression : assignment_expression
                  | expression COMMA assignment_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('comma', p[1], p[3])


def p_assignment_expression(p):
    '''assignment_expression : ID ASSIGN assignment_expression
                             | logical_or_expression'''
    if len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = p[1]


def p_logical_or_expression(p):
    '''logical_or_expression : logical_and_expression
                             | logical_or_expression OR logical_and_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('or', p[1], p[3])


def p_logical_and_expression(p):
    '''logical_and_expression : equality_expression
                              | logical_and_expression AND equality_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('and', p[1], p[3])


def p_equality_expression(p):
    '''equality_expression : relational_expression
                           | equality_expression EQ relational_expression
                           | equality_expression NEQ relational_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_relational_expression(p):
    '''relational_expression : additive_expression
                             | relational_expression LT additive_expression
                             | relational_expression LE additive_expression
                             | relational_expression GT additive_expression
                             | relational_expression GE additive_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                           | additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                 | multiplicative_expression MULT unary_expression
                                 | multiplicative_expression DIV unary_expression
                                 | multiplicative_expression MOD unary_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_postfix_expression(p):
    '''postfix_expression : primary_expression
                          | postfix_expression LPAREN argument_expression_list_opt RPAREN
                          | postfix_expression INCREMENT
                          | postfix_expression DECREMENT'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '(':
        p[0] = ('call', p[1], p[3])
    elif p[2] == '++':
        p[0] = ('post_inc', p[1])  
    elif p[2] == '--':
        p[0] = ('post_dec', p[1])


def p_argument_expression_list_opt(p):
    '''argument_expression_list_opt : argument_expression_list
                                    | empty'''
    p[0] = p[1] if p[1] is not None else []


def p_argument_expression_list(p):
    '''argument_expression_list : assignment_expression
                                | argument_expression_list COMMA assignment_expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_unary_expression(p):
    '''unary_expression : postfix_expression
                        | PLUS unary_expression
                        | MINUS unary_expression
                        | NOT unary_expression
                        | INCREMENT unary_expression
                        | DECREMENT unary_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        op_map = {'++': 'pre_inc', '--': 'pre_dec', '!' : 'not', '+' : 'uplus', '-' : 'uminus'}
        p[0] = (op_map.get(p[1]),  p[2])


def p_primary_expression(p):
    '''primary_expression : ID
                          | constant
                          | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]
        

def p_selection_statement(p):
    '''selection_statement : IF LPAREN expression RPAREN statement
                           | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])


def p_iteration_statement(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN statement
                           | FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
    if p[1] == 'while':
        p[0] = ('while', p[3], p[5])
    else:
        p[0] = ('for', p[3], p[4], p[5], p[7])


def p_jump_statement(p):
    '''jump_statement : RETURN expression SEMI
                      | BREAK SEMI
                      | CONTINUE SEMI'''
    p[0] = tuple(p[1:])

def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if not p:
        error_details = {'type': 'Erro de Sintaxe', 'value': 'EOF', 'line': lexer.lineno, 'column': 'N/A', 'message': 'Final de arquivo inesperado.'}
        parse_error.append(error_details)
        return

    col = find_collum(lexer.lexdata, p)
    error_details = {'type': 'Erro de Sintaxe', 'value': p.value, 'line': p.lineno, 'column': col, 'message': f"Token inesperado '{p.value}'"}
    parse_error.append(error_details)
    # Tenta se recuperar para encontrar mais erros
    while True:
        tok = parser.token()
        if not tok or tok.type in ('SEMI', 'RBRACE'): break
    parser.errok()
    return tok




parser = yacc.yacc()
