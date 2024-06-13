import ply.lex as lex

# Lista de palabras reservadas y tokens para JavaScript
reserved = {
    'for': 'FOR',
    'system': 'SYSTEM',
    'System': 'SYSTEM',  # Añadido para manejar 'System' con mayúscula
    'out': 'OUT',
    'println': 'PRINTLN'
}

# Lista de tokens para JavaScript
tokens = [
    'ID',
    'NUMBER',
    'EQUALS',
    'LESS_THAN_EQUAL',
    'INCREASE',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON',
    'DOT',
] + list(reserved.values())

# Expresiones regulares para los nuevos tokens
t_EQUALS = r'='
t_LESS_THAN_EQUAL = r'<='
t_INCREASE = r'\+\+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_DOT = r'\.'

# Expresión regular para identificar números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para manejar identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Incrementar número de línea en caracteres de nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados
t_ignore = ' \t'

# Regla de error
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
