from callable import LoxCallable
from instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name

    def find_method(self, name):
        try:
            if self.methods[name] is not None:
                return self.methods[name]
        except KeyError:
            pass
        
    def call(self, interpreter, arguments):
        instance = LoxInstance(self)

        initializer = self.find_method('init')
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self):
        initializer = self.find_method('init')
        if initializer is not None:
            return initializer.arity()
        return 0