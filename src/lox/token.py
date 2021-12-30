class Token:
    def __init__(self, type_, lexeme, literal, line):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        if self.lexeme:
            return f'{self.type}:{self.lexeme}:{self.literal}'
        return f'{self.type}'

token_types = {
    #Single-character tokens.
    '(': 'LEFT_PAREN',
    ')': 'RIGHT_PAREN',
    '{': 'LEFT_BRACE',
    '}': 'RIGHT_BRACE',
    ',': 'COMMA',
    '.': 'DOT',
    '-': 'MINUS',
    '+': 'PLUS',
    ';': 'SEMICOLON',
    '/': 'SLASH',
    '*': 'STAR',

    # One or two character tokens.
    '!': 'BANG',
    '!=': 'BANG_EQUAL',
    '=': 'EQUAL',
    '==': 'EQUAL_EQUAL',
    '>': 'GREATER',
    '>=': 'GREATER_EQUAL',
    '<': 'LESS',
    '<=': 'LESS_EQUAL',

     # Literals.
    'IDENTIFIER': 'IDENTIFIER',
    'STRING': 'STRING',
    'NUMBER': 'NUMBER',

    # Keywords
    'and': 'AND',
    'class' : 'CLASS',
    'else' : 'ELSE',
    'false' : 'FALSE',
    'fun' : 'FUN',
    'for' : 'FOR',
    'if' : 'IF',
    'nil' : 'NIL',
    'or' : 'OR',
    'print' : 'PRINT',
    'return' : 'RETURN',
    'super' : 'SUPER',
    'this' : 'THIS',
    'true' : 'TRUE',
    'var' : 'VAR',
    'while' : 'WHILE',

    'EOF': 'EOF'
}
