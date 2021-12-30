from expr import *
from stmt import *
from printer import Printer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def declaration(self):
        try:
            if self.match('FUN'):
                return self.function('function')
            if self.match('VAR'): 
                return self.var_declaration()
            else:
                print('state', self.statement())
                return self.statement()
        except:
            self.synchronize()
            return

    def function(self, kind):
        name = self.consume('IDENTIFIER', f'Expect {kind} name.')

        self.consume('LEFT_PAREN', f'Expect "(" after {kind} name.')
        parameters = []
        if not self.check('RIGHT_PAREN'):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), 'Cant have more than 255 parameters')
                parameters.append(self.consume('IDENTIFIER', 'Expect parameter name'))
                if not self.match('COMMA'):
                    break
        self.consume('RIGHT_PAREN', f"Expect ')' after parameters")
        self.consume('LEFT_BRACE', 'Expect "{" before ', {kind}, ' body.')
        body = self.block()
        return Function(name, parameters, body)

    def var_declaration(self):
        name = self.consume('IDENTIFIER', 'Expect a variable name')

        initializer = None
        if self.match('EQUAL'):
            initializer = self.expression()

        self.consume('SEMICOLON', 'Expect a ";" after variable declaration')
        return Var(name, initializer)

    def statement(self):
        if self.match('PRINT'): return self.print_statement()
        if self.match('LEFT_BRACE'): return Block(self.block())
        if self.match('IF'): return self.if_statement()
        if self.match('WHILE'): return self.while_statement()
        if self.match('FOR'): return self.for_statement()
        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume('SEMICOLON', 'Expected ";" after a value')
        return Print(value)

    def expression_statement(self):
        expr = self.expression()
        self.consume('SEMICOLON', 'Expected ";" after a expression')
        return Expression(expr)

    def block(self):
        statements = []

        while not self.is_at_end() and not self.check('RIGHT_BRACE'):
            statements.append(self.declaration())

        self.consume('RIGHT_BRACE', 'Expect "}" after block.')
        return statements

    def if_statement(self):
        self.consume('LEFT_PAREN', 'Expect "(" after if.')
        condition = self.expression()
        self.consume('RIGHT_PAREN', 'Expect ")" after if condition.')

        then_branch = self.statement()
        else_branch = None

        if self.match('ELSE'): else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume('LEFT_PAREN', 'Expect "(" after while')
        condition = self.expression()
        self.consume('RIGHT_PAREN', 'Expect ")" after while condition.')
        body = self.statement()

        return While(condition, body)

    def for_statement(self):
        self.consume('LEFT_PAREN', 'Expect "(" after for')

        initializer = None
        if self.match('VAR'):
            initializer = self.var_declaration()
        else: initializer = self.expression_statement()

        condition = None
        if not self.check('SEMICOLON'):
            condition = self.expression()
        self.consume('SEMICOLON', 'Expect ";" after loop condition.')

        increment = None
        if not self.check('RIGHT_PAREN'):
            increment = self.expression()
        self.consume('RIGHT_PAREN', 'Expect ")" after for clauses')

        body = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Litera(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])

        return body

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.or_()

        if self.match('EQUAL'):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, 'Invalid assignment target.')

        return expr
    
    def or_(self):
        expr = self.and_()

        while self.match('OR'):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)
        
        return expr

    def and_(self):
        expr = self.equality()

        while self.match('AND'):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr

    def equality(self):
        expr = self.comparison()

        while self.match('BANG_EQUAL', 'EQUAL_EQUAL'):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match('GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL'):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match('MINUS', 'PLUS'):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match('SLASH', 'STAR'):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match('BANG', 'MINUS'):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match('LEFT_PAREN'):
                expr = self.finish_call(expr)
            else: 
                break

        return expr

    def primary(self):
        if self.match('FALSE'): return Literal(False)
        if self.match('TRUE'): return Literal(True)
        if self.match('NIL'): return Literal(None)

        if self.match('NUMBER', 'STRING'):
            return Literal(self.previous().literal)
        if self.match('IDENTIFIER'): 
            return Variable(self.previous())

        if self.match('LEFT_PAREN'):
            expr = self.expression()
            self.consume('RIGHT_PAREN', 'Expect ")" after expression')
            return Grouping(expr)

        raise self.error(self.peek(), 'Expected expression.')
        return


    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == 'EOF'

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, type, message):
        if self.check(type):
            return self.advance()

        raise self.error(self.peek(), message)
        return

    def finish_call(self, callee):
        arguments = []

        if not self.check('RIGHT_PAREN'):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments")
                arguments.append(self.expression())
                if not self.match('COMMA'):
                    break

        paren = self.consume('RIGHT_PAREN', 'Expect ")" after arguments.')

        return Call(callee, paren, arguments)

    def error(self, token, message):
        # Lox.error(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == 'SEMICOLON': return
            if self.peek().type in ['CLASS','FUN','VAR','FOR','IF','WHILE','PRINT','RETURN']: return

        self.advance()

class ParseError(RuntimeError):
    def __init__(self):
        super().__init__()
