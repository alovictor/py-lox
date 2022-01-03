from lexer import Lexer
from parser import Parser
from printer import Printer
from interpreter import Interpreter

class Lox:
    had_error = False
    had_runtime_error = False

    @staticmethod
    def run_file(path):
        bytes = ''
        with open(path, 'rb') as file:
            bytes = file.read().decode('UTF-8')

        Lox.run(bytes)

    @staticmethod
    def run_prompt():
        while True:
            command = input('lox > ')
            Lox.run(command)

    @staticmethod
    def run(source):
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        # print(tokens)

        parser = Parser(tokens)
        statements = parser.parse()
        # print(statements)

        if Lox.had_error: return
        if Lox.had_runtime_error: return
        Interpreter().interpret(statements)

    @staticmethod
    def runtime_error(error):
        print(f'[line {error.token.line}]')
        Lox.had_runtime_error = True

    @staticmethod
    def error(token, message):
        if token.type == 'EOF':
            Lox.report(token.line," at end", message)
        else:
            Lox.report(token.line, " at '" + token.lexeme + "'", message)

    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True
