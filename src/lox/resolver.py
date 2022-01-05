from expr import ExprVisitor
from stmt import StmtVisitor

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = 'NONE'
        self.current_class = 'NONE'

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve_statements(stmt.statements)
        self.end_scope()
        return None

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)

        if stmt.initializer is not None:
            self.resolve_expression(stmt.initializer)

        self.define(stmt.name)
        return None

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, 'FUNCTION')
        return None

    def visit_class_stmt(self, stmt):
        self.current_class = 'CLASS'

        self.declare(stmt.name)
        self.define(stmt.name)

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            declaration = 'METHOD'
            if method.name.lexeme == 'init':
                declaration = 'INITIALIZER'
            self.resolve_function(method, declaration)

        self.end_scope()
        self.current_class = 'NONE'
        return None

    def visit_get_expr(self, expr):
        self.resolve(expr.object)
        return None
    
    def visit_set_expr(self, expr):
        self.resolve_expression(expr.value)
        self.resolve_expression(expr.object)
        return None

    def visit_this_expr(self, expr):
        if self.current_class == 'NONE':
            print('Cant use this outside a class')
            return None

        self.resolve_local(expr, expr.keyword)
        return None

    def visit_expression_stmt(self, stmt):
        self.resolve_expression(stmt.expression)
        return None

    def visit_if_stmt(self, stmt):
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.then_branch)
        if stmt.else_branch != None:
            self.resolve_statement(stmt.else_branch)

        return None

    def visit_print_stmt(self, stmt):
        self.resolve_expression(stmt.expression)
        return None

    def visit_return_stmt(self, stmt):
        if self.current_function == 'NONE':
            print('Cant return from top-level code.')
        if stmt.value != None:
            if self.current_function == 'INITIALIZER':
                print('Cant return a value from an initializer')
                return None
            self.resolve_expression(stmt.value)

        return None

    def visit_while_stmt(self, stmt):
        self.resolve_expression(stmt.condition)
        self.resolve_statement(stmt.body)
        return None

    def visit_variable_expr(self, expr):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) == False:
            print(f'Cant reload local variable in its own initializer')

        self.resolve_local(expr, expr.name)
        return None

    def visit_assign_expr(self, expr):
        self.resolve_expression(expr.name)
        self.resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)
        return None

    def visit_call_expr(self, expr):
        self.resolve_expression(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)

        return None

    def visit_grouping_expr(self, expr):
        self.resolve_expression(expr.expression)
        return None

    def visit_literal_expr(self, expr):
        return

    def visit_logical_expr(self, expr):
        self.resolve_expression(expr.left)
        self.resolve_expression(expr.right)
        return None

    def visit_unary_expr(self, expr):
        self.resolve_expression(expr.right)
        return None

    def declare(self, name):
        if len(self.scopes) == 0:
            return
    
        scope = self.scopes[-1] # Get the top of the scope stack
        if name.lexeme in scope:
            print(f"Variable {name.lexeme} already defined in the current scope")
        
        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve(self, stmts):
        self.resolve_statements(stmts)

    def resolve_statements(self, stmts):
        if not isinstance(stmts, list):
            self.resolve_statement(stmts)
            return None
        for statement in stmts:
            self.resolve_statement(statement)

    def resolve_statement(self, stmt):
        stmt.accept(self)

    def resolve_expression(self, expr):
        expr.accept(self)

    def resolve_local(self, expr, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
                return

    def resolve_function(self, function, type_):
        enclosing_function = self.current_function
        self.current_function = type_

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        
        self.resolve_statements(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    