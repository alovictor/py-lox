class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def __str__(self):
        return f'{self.klass.name} instance'

    def get(self, name):
        try:
            return self.fields[name.lexeme]
        except KeyError:
            pass

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        print(f'Undefined field {name.lexeme}.')

    def set(self, name, value):
        self.fields[name.lexeme] = value