class SemanticAnalyzer:
    def __init__(self):
        self.variables = set()

    def analyze(self, ast):
        self.visit(ast)

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_ForStatement(self, node):
        # Verificar la declaración y el alcance de la variable en el bucle for
        if node.variable not in self.variables:
            raise ValueError(f"Variable '{node.variable}' no declarada en el ámbito actual.")
        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.body)

    def visit_Assignment(self, node):
        # Registrar la declaración de variables
        self.variables.add(node.variable)
        self.visit(node.value)

    def visit_Number(self, node):
        # Verificar el tipo de datos de los números
        if not isinstance(node.value, int):
            raise ValueError("Los números deben ser de tipo entero.")

    # Agregar métodos de visita para otros nodos del AST según sea necesario
