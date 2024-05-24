import ply.lex as lex
import ply.yacc as yacc

# Lex token 
tokens = (
    'ID',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
    'EQUALS',
    'LESS_THAN',
    'GREATER_THAN',
    'LE',
    'GE',
    'NE',
    'PLUS',
    'MINUS',
    'PLUS_PLUS',
    'MINUS_MINUS',
    'NUMBER',
    'INT_TYPE',
    'FLOAT_TYPE',
    'STRING_TYPE',
    'VOID_TYPE',
    'PUBLIC',
    'FOR',
    'IF',
)

# Reserved
reserved = {
    'int': 'INT_TYPE',
    'float': 'FLOAT_TYPE',
    'string': 'STRING_TYPE',
    'void': 'VOID_TYPE',
    'public': 'PUBLIC',
    'for': 'FOR',
    'if': 'IF',
}

# Regex
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN=r'>'
t_LE=r'<='
t_GE=r'>='
t_NE=r'!='
t_PLUS = r'\+'
t_MINUS = r'\-'
# t_PLUS_PLUS=r'++'
t_MINUS_MINUS=r'--'
t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def p_program(p):
    '''
    program : declaration
            | function_declaration
            | for_loop
            | if_statement
    '''
    print(p[1])

def p_declaration(p):
    '''
    declaration : simple_declaration
                | array_declaration
    '''
    p[0] = p[1]

def p_type(p):
    '''
    type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | VOID_TYPE
    '''
    p[0] = p[1]

def p_simple_declaration(p):
    'simple_declaration : type ID SEMICOLON'
    p[0] = f"Simple Declaration: {p[2]} is of type {p[1]}"

def p_array_declaration(p):
    'array_declaration : type LBRACKET RBRACKET ID SEMICOLON'
    p[0] = f"Array Declaration: {p[4]} is an array of type {p[1]}"

def p_function_declaration(p):
    'function_declaration : PUBLIC type ID LPAREN parameters RPAREN SEMICOLON'
    p[0] = f"Function Declaration: {p[3]} is a function returning {p[2]} with parameters {p[5]}"

def p_parameters(p):
    '''
    parameters : parameter
            | parameter COMMA parameters
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parameter(p):
    'parameter : type ID'
    p[0] = f"{p[1]} {p[2]}"

def p_sym(p):
    '''
    sym : LESS_THAN
        | GREATER_THAN
        | GE
        | LE
        | NE
        
'''
    p[0] = p[1]

def p_for_loop(p):
    'for_loop : FOR LPAREN type ID EQUALS NUMBER SEMICOLON ID sym ID SEMICOLON ID inc RPAREN'
    p[0] = f"For Loop: for({p[3]} = {p[6]}; {p[8]} {p[9]} {p[10]}; {p[12]} {p[13]})"

def p_if_statement(p):
    'if_statement : IF LPAREN condition RPAREN'
    p[0] = f"If Statement: if({p[3]})"

def p_condition(p):
    'condition : ID sym comp'
    p[0] = f"{p[1]} {p[2]} {p[3]}"
    
def p_comp(p):
    '''
    comp : ID
        | NUMBER
'''
    p[0]=p[1]

def p_inc(p):
    '''
    inc : MINUS MINUS
        | PLUS PLUS
    '''
    p[0]=p[1]

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}: Unexpected token '{p.value}'")
    else:
        print("Syntax error at EOF")

lexer = lex.lex()

parser = yacc.yacc()

while True:
    user_input = input("Enter a declaration (or 'exit' to quit): ")
    if user_input == 'exit':
        break

    lexer.input(user_input)
    while True:
        tok = lexer.token()
        if not tok:
            break  # No input
        print(tok)

    result = parser.parse(user_input)
    if result:
        print(result)
