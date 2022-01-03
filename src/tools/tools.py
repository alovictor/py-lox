class GenerateAST:
    def main(self, args):
        if len(args) != 1:
            print("Usage: generate_ast <output directory>")
            exit()

        self.output_dir = args[0]

        self.define_ast(self.output_dir, "Expr", [
            "Assign   : name, value",
            "Binary   : left, operator, right",
            "Grouping : expression",
            "Literal  : value",
            "Logical  : left, operator, right",
            "Unary    : operator, right",
            "Variable : name",
            "Call     : callee, paren, arguments",
        ])

        self.define_ast(self.output_dir, 'Stmt', [
            "Block      : statements",
            "Expression : expression",
            "If         : condition, then_branch, else_branch",
            "Print      : expression",
            "Var        : name, initializer",
            "While      : condition, body",
            "Function   : name, params, body",
            "Return     : keyword, value",
            
        ])

    def define_ast(self, output_dir, base_name, types):
        path = f'{output_dir}/{base_name.lower()}.py'

        with open(path, 'w') as file:
            self.define_imports(file)
            self.define_visitor(file, base_name, types)

            file.write(f'class {base_name}(ABC):\n')
            file.write(f'   @staticmethod\n')
            file.write(f'   def accept(self, visitor):\n')
            file.write(f'       pass\n\n')

            for type in types:
                class_name = type.split(':')[0].strip()
                fields = type.split(':')[1].strip()
                file.write(f'class {class_name}({base_name}):\n')
                file.write(f'   def __init__(self, {fields}):\n')
                fields = fields.split(', ')
                for field in fields:
                    file.write(f'       self.{field} = {field}\n')
                file.write('\n')
                file.write(f'   def accept(self, visitor):\n')
                file.write(f'       return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)\n\n')


    def define_imports(self, file):
        file.write(f'from abc import ABC, abstractmethod\n\n')

    def define_visitor(self, file, base_name, types):
        file.write(f'class {base_name}Visitor(ABC):\n')
        for type in types:
            type_name = type.split(':')[0].strip()
            file.write(f'   @abstractmethod\n')
            file.write(f'   def visit_{type_name.lower()}_{base_name.lower()}(self, {base_name.lower()}):\n')
            file.write(f'       pass\n\n')

if __name__ == '__main__':
    gen = GenerateAST()
    gen.main(['/home/victo/dev/python/lox/src/lox'])
