from expr import *
from stmt import *
from callable import *
from environment import Environment

class LoxRuntimeError(RuntimeError):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()

        self.globals.define("clock", LoxClock())

        self.environment = self.globals

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except:
            raise LoxRuntimeError(None, message='Erro')

    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, statements, env):
        previous = self.environment
        self.environment = env

        for state in statements:
            self.execute(state)
        
        self.environment = previous

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringfy(value))
        return None

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(enclosing = self.environment))
        return None

    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.execute(stmt.else_branch)
        return None

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_call_expr(self, expr):
        print('call')
        callee = self.evaluate(expr)

        arguments = []
        for argument in arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, message="Can only call functions and classes.")

        if len(arguments) != funcion.arity():
            raise LoxRuntimeError(expr.paren, message=f"Expected {function.arity} arguments but got {len(arguments)}.")

        return callee.call(self, arguments)


    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == 'MINUS':
            self.check_number_operand(expr.operator, right)
            return float(-right)
        elif expr.operator.type == 'BANG':
            return not self.is_truthy(right)

        return None

    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if   expr.operator.type == 'MINUS':
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == 'SLASH':
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type == 'STAR' :
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == 'PLUS':
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            if isinstance(left, str) and isinstance(right, float):
                return str(left) + self.stringfy(right)
            if isinstance(left, float) and isinstance(right, str):
                return self.stringfy(left) + str(right)
            raise LoxRuntimeError(expr.operator, 'Operands must be two numbers or two strings.')
        elif expr.operator.type == 'GREATER' :
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == 'GREATER_EQUAL' :
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == 'LESS' :
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == 'LESS_EQUAL' :
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == 'BANG_EQUAL' : return not self.is_equal(left, right)
        elif expr.operator.type == 'EQUAL_EQUAL' : return self.is_equal(left, right)

        return None

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == 'OR':
            if self.is_truthy(left): return left
        else:
            if not self.is_truthy(left): return left

        return self.evaluate(expr.right)

    def evaluate(self, expr):
        return expr.accept(self)

    def is_truthy(self, obj):
        if obj == None: return False
        if isinstance(obj, bool): return bool(obj)
        return True

    def is_equal(self, a, b):
        if a == None and b == None: return True
        elif a == None: return False
        return a == b

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float): return
        raise LoxRuntimeError(operator, 'Operand must be a number.')

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float): return
        raise LoxRuntimeError(operator, 'Operands must be numbers.')

    def stringfy(self, obj):
        if obj == None: return 'nil'

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith('.0'):
                text = text[:len(text)-2]
            return text
        return str(obj)
