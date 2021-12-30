from sys import argv

from lox import Lox

def main(args):

    if len(args) > 1:
        print('Usage: lox [script]')
        exit()

    elif len(args) == 1:
        Lox.run_file(args[0])
        
    else:
        Lox.run_prompt()


main(argv[1:])
