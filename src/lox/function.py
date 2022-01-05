from callable import LoxCallable
from returnerr import ReturnErr
from environment import Environment

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def __repr__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        

        for i, params in enumerate(self.declaration.params):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnErr as e:
            if self.is_initializer:
                return self.closure.get_at(0, 'this')
            return e.value

        if self.is_initializer:
            return self.closure.get_at(0, 'this')

        return None

    def arity(self):
        return len(self.declaration.params)

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)