from token import Token, token_types

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token('EOF', '', None, self.line))

        return self.tokens

    def scan_token(self):
        c = self.advance()

        if   c in '(){},.-+;*!=<>/' : self.single_char()
        elif c in ' \r\t': pass
        elif c == '\n': self.line += 1
        elif c == '"': self.string()
        elif c.isdigit(): self.number()
        elif c.isalpha(): self.identifier()

    def add_token(self, type, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected):
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return '\n'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def single_char(self):
        if self.match('='):
            text = self.source[self.current - 2] + self.source[self.current - 1]
        elif self.match('/'):
            while self.peek() != '\n': self.advance()
            return
        else:
            text = self.source[self.current - 1]

        self.add_token(token_types[text])

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            return

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token('STRING', value)

    def number(self):
        while self.peek().isdigit(): self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit(): self.advance()

        self.add_token('NUMBER', float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum(): self.advance()

        text = self.source[self.start:self.current]
        try:
            type = token_types[text]
        except:
            type = 'IDENTIFIER'

        self.add_token(type)
