from callable import LoxCallable
from returnerr import ReturnErr
from environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        

        for i, params in enumerate(self.declaration.params):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnErr as e:
            return e.value

        return None

    def arity(self):
        return len(self.declaration.params)

    def to_string(self):
        return f"<fn {self.declaration.name.lexeme}>"