class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeError(f'Undefined variable "{name.lexeme}".')

    def define(self, name, value):
        self.values[name] = value

    def get_at(self, distance, name):
        return self.ancestor(distance).values.get(name)
        
    def ancestor(self, distance):
        enviorment = self
        
        for i in range(distance):
            enviorment = enviorment.enclosing
        
        return enviorment

    def assign(self, name, value):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(f'Undefined variable "{name.lexeme}".')

    def assign_at(self, distance, name, value):
        self.ancestor(distance).values[name.lexeme] = value
