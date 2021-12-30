from callable import LoxCallable
from environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)

        for i in range(len(self.declaration.params)):
            self.environment.define(self.declaration.params.get(i).lexeme, arguments.get(i))

        self.interpreter.execute_block(self.declaration.body, self.environment)
        return None

    def arity(self):
        return len(self.declaration.params)

    def to_string(self):
        return f"<fn {self.declaration.name.lexeme}>"