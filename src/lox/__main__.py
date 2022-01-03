from sys import argv
from lox import Lox

try:
    if len(argv) > 2:
        print('Usage: seven [script]')
    elif len(argv) == 2:
        Lox.run_file(argv[1])
    else:
        Lox.run_prompt()
        
except KeyboardInterrupt:
    print('\n')
    exit()
