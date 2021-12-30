from expr import *
from token import *

class Printer(ExprVisitor):
    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs):
        content = ' '.join(expr.accept(self) for expr in exprs)

        return f'({name} {content})'

    def visit_binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value == None:
            return 'nil'
        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)


if __name__ == '__main__':
    exp = Binary(
            Unary(
                Token('MINUS', '-', None, 1),
                Literal(123)),
            Token('STAR', '*', None, 1),
            Grouping(
                Literal(45.93))
    )

    printer = Printer()
    print(printer.print(exp))
