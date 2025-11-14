import os
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .runtime import Context, SymbolTable
from .values import Number, String, BuiltInFunction

# Global symbols and built-ins for the LRL language
global_symbol_table = SymbolTable()
# booleans and constants
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
# builtins matching sample.lrl API
global_symbol_table.set("say", BuiltInFunction.say)
global_symbol_table.set("get_int", BuiltInFunction.get_int)
global_symbol_table.set("get_float", BuiltInFunction.get_float)
global_symbol_table.set("get_string", BuiltInFunction.get_string)

# --- Runner functions ---

def run_text(fn: str, text: str):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table

    result = interpreter.visit(ast.node, context)
    return result.value, result.error

def run_file(path: str):
    if not path.endswith('.lrl'):
        raise SystemExit('Only .lrl files are allowed')
    if not os.path.exists(path):
        raise SystemExit(f'File not found: {path}')
    with open(path, 'r') as f:
        code = f.read()
    return run_text(path, code)
