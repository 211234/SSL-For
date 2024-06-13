from flask import Flask, render_template, request, redirect, url_for
from lexer_js import lexer
from parser_js import parser, semantic_analyze

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', tokens=[], errors=[], success=None)

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.form['code']
    lexer.lineno = 1  # Reiniciar el número de línea
    lexer.input(code)
    
    tokens = []
    errors = []
    success = None
    
    # Análisis léxico
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append({
            'line': tok.lineno,
            'position': tok.lexpos,
            'type': tok.type,
            'value': tok.value
        })
    
    total_tokens = len(tokens)
    
    # Análisis sintáctico y semántico
    try:
        ast = parser.parse(code)
        semantic_analyze(ast)
        success = "El código JavaScript es correcto."
    except SyntaxError as e:
        errors.append(str(e))
    except Exception as e:
        errors.append(f"Error no especificado: {str(e)}")
    
    return render_template('index.html', tokens=tokens, errors=errors, success=success, code=code, total_tokens=total_tokens)

@app.route('/reset')
def reset():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
