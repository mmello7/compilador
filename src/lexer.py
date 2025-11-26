import ply.lex as lex

lex_error = []
symbol_table= []

tokens = [
    
    'AUTO','BREAK','CASE','CHAR','CONST','CONTINUE','DEFAULT','DO','DOUBLE','ELSE',
    'ENUM','EXTERN','FLOAT','FOR','GOTO','IF','INLINE','INT','LONG','REGISTER','RESTRICT',
    'RETURN','SHORT','SIGNED','SIZEOF','STATIC','STRUCT','SWITCH','TYPEDEF','UNION',
    'UNSIGNED','VOID','VOLATILE','WHILE',

    'ID','NUMBER','FLOATNUM','CHAR_CONST','STRING',

    'PLUS','MINUS','MULT','DIV','MOD','INCREMENT','DECREMENT',

    'EQ','NEQ','LT','LE','GT','GE',

    'AND','OR','NOT',

    'BITAND','BITOR','BITXOR','BITNOT','LSHIFT','RSHIFT',

    'ASSIGN','PLUS_ASSIGN','MINUS_ASSIGN','MULT_ASSIGN','DIV_ASSIGN','MOD_ASSIGN',
    'AND_ASSIGN','OR_ASSIGN','XOR_ASSIGN','LSHIFT_ASSIGN','RSHIFT_ASSIGN',

    'LPAREN','RPAREN','LBRACE','RBRACE','LBRACKET','RBRACKET','SEMI','COMMA', 'QUESTION', 'COLON', 'HASH'
]

reserved = {
    'auto':'AUTO','break':'BREAK','case':'CASE','char':'CHAR','const':'CONST',
    'continue':'CONTINUE','default':'DEFAULT','do':'DO','double':'DOUBLE','else':'ELSE',
    'enum':'ENUM','extern':'EXTERN','float':'FLOAT','for':'FOR','goto':'GOTO',
    'if':'IF','inline':'INLINE','int':'INT','long':'LONG','register':'REGISTER',
    'restrict':'RESTRICT','return':'RETURN','short':'SHORT','signed':'SIGNED',
    'sizeof':'SIZEOF','static':'STATIC','struct':'STRUCT','switch':'SWITCH',
    'typedef':'TYPEDEF','union':'UNION','unsigned':'UNSIGNED','void':'VOID',
    'volatile':'VOLATILE','while':'WHILE'
}

t_INCREMENT     = r'\+\+'
t_DECREMENT     = r'--'

t_LSHIFT_ASSIGN = r'<<='
t_RSHIFT_ASSIGN = r'>>='
t_PLUS_ASSIGN   = r'\+='
t_MINUS_ASSIGN  = r'-='
t_MULT_ASSIGN   = r'\*='
t_DIV_ASSIGN    = r'/='
t_MOD_ASSIGN    = r'%='
t_AND_ASSIGN    = r'&='
t_OR_ASSIGN     = r'\|='
t_XOR_ASSIGN    = r'\^='

t_LSHIFT        = r'<<'
t_RSHIFT        = r'>>'

t_LE            = r'<='
t_GE            = r'>='
t_EQ            = r'=='
t_NEQ           = r'!='
t_LT            =r'<'
t_GT            =r'>'

t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

t_BITAND        = r'&'
t_BITOR         = r'\|'
t_BITXOR        = r'\^'
t_BITNOT        = r'~'

t_ASSIGN        = r'='

t_PLUS          = r'\+'
t_MINUS         = r'-'
t_MULT          = r'\*'
t_DIV           = r'/'
t_MOD           = r'%'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI    = r';'
t_COMMA   = r','

t_QUESTION = r'\?'
t_COLON = r':'
t_HASH = r'\#'


def t_FLOATNUM(t):
    r'\d+\.\d*([eE][+-]?\d+)? | \.\d+([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_CONST(t):
    r"'(\\.|[^\\'])'"
    return t

def t_STRING(t):
    r'"(\\.|[^"\\])*"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')

    if t.type == 'ID':
        if t.value not in symbol_table:
            symbol_table.append(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'//.*'
    pass

def t_BLOCK_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def find_collum(text, token): #para calcular a coluna de erro pois a biblioteca ply so mostra a linha
    last_cr = text.rfind('\n', 0, token.lexpos)
    if last_cr <0:
        last_cr = -1
    return (token.lexpos - last_cr)

def t_STRING_UNCLOSED(t):
    r'\"[^\n]*\n'
    text = t.lexer.lexdata
    col = find_collum(text, t)
    error_details = {
        'type': 'String mal formada',
        'value': t.value.strip(),
        'line': t.lineno,
        'column': col,
        'message': 'A String não foi fechada corretamente'
    }
    lex_error.append(error_details)
    t.lexer.lineno += 1

def t_CHAR_CONST_UNCLOSED(t):
     r'\'[^\n]*\n'
     text = t.lexer.lexdata
     col = find_collum(text, t)
     error_details = {
        'type': 'Caractere ilegal',
        'value': t.value[0],
        'line': t.lineno,
        'column': col,
        'message': 'A constante de caractere não foi fechada na mesma linha'
        }
     lex_error.append(error_details)
     t.lexer.lineno += 1
     t.lexer.skip(1)

def t_error(t):
    col = find_collum(t.lexer.lexdata, t)
    error_details = {'type': 'Caractere Ilegal', 'value': t.value[0], 'line': t.lineno, 'column': col}
    lex_error.append(error_details)
    t.lexer.skip(1)
    
lexer = lex.lex()
