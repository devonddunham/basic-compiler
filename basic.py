from lex import *
from parse import *
from emit import *
import sys

def main():
    print("Basic Compiler")

    # check for source file in command line args
    if len(sys.argv) != 2:
        sys.exit("Usage: basic.py <sourcefile>")
    with open(sys.argv[1], 'r') as f:
        source = f.read()
    
    # init lexer and parser
    lexer = Lexer(source)
    emitter = Emitter("out.cpp")
    parser = Parser(lexer, emitter)

    # parse the source code
    parser.program() # start
    emitter.write_file() # write to file
    print("Parsing complete.")

if __name__ == "__main__":
    main()
