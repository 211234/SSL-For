import ply.yacc as yacc
from lexer_js import tokens

class Program:
    def __init__(self, stmts):
        self.stmts = stmts

class StmtList:
    def __init__(self, *stmts):
        self.stmts = stmts

class ForStatement:
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

class PrintStatement:
    def __init__(self, variable):
        self.variable = variable

def p_program(p):
    '''program : stmts'''
    p[0] = Program(p[1])

def p_stmts(p):
    '''stmts : stmt
             | stmts stmt'''
    if len(p) == 2:
        p[0] = StmtList(p[1])
    else:
        p[0] = StmtList(*p[1].stmts, p[2])

def p_stmt(p):
    '''stmt : for_stmt
            | system_out_println'''
    p[0] = p[1]

def p_for_stmt(p):
    '''for_stmt : FOR LPAREN ID EQUALS NUMBER SEMICOLON ID LESS_THAN_EQUAL NUMBER SEMICOLON ID INCREASE RPAREN LBRACE stmts RBRACE'''
    if p[3] != p[7] or p[3] != p[11]:
        raise SyntaxError(f"Error de sintaxis en la línea {p.lineno(3)}: las variables en el bucle 'for' deben ser iguales.")
    p[0] = ForStatement(p[3], p[5], p[9], p[15])

def p_system_out_println(p):
    '''system_out_println : SYSTEM DOT OUT DOT PRINTLN LPAREN ID RPAREN SEMICOLON'''
    p[0] = PrintStatement(p[7])

def p_error(p):
    if not p:
        raise SyntaxError("Error de sintaxis: se esperaba un componente, pero el archivo terminó de forma inesperada.")
    else:
        raise SyntaxError(f"Error de sintaxis en la línea {p.lineno}: no se reconoce el token '{p.value}'.")

# Construir el parser
parser = yacc.yacc()

# Función de análisis semántico
def semantic_analyze(ast):
    declared_variables = set()

    def analyze_node(node):
        if isinstance(node, Program):
            for stmt in node.stmts.stmts:
                analyze_node(stmt)
        elif isinstance(node, StmtList):
            for stmt in node.stmts:
                analyze_node(stmt)
        elif isinstance(node, ForStatement):
            declared_variables.add(node.variable)
            analyze_node(node.body)
        elif isinstance(node, PrintStatement):
            if node.variable not in declared_variables:
                raise Exception(f"Variable '{node.variable}' no declarada.")
        else:
            raise Exception("Nodo no reconocido en el análisis semántico.")

    analyze_node(ast)
