from expr import ExprVisitor

class Resolver(ExprVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scope = []

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt)
        self.end_scope()
        return None

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)

        if stmt.initializer is not None:
            self.resolve(stmt.initializer)

        self.define(stmt.name)
        return None

    def declare(self, name):
        if self.scopes:
            scope = self.scopes[-1] # Get the top of the scope stack
            if name.lexeme in scope:
                print(name, f"Variable {name.lexeme} already defined in the current scope")
            else:
                scope[name.lexeme] = False

                # parei aqui
    
    def resolve(self, stmt):
        for statement in stmt:
            self.resolve_stmt(statement)

    def resolve_stmt(self, stmt):
        stmt.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    