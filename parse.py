import sys
from lex import *

# Parser class
# object keeps track of the current token and checks if the code matches the grammar
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.cur_token = None
        self.peek_token = None
        self.next()
        self.next() # call twice to set up the lookahead


    # return true if the current token matches
    def check_token(self, kind):
        return kind == self.cur_token.kind

    # return true if the next token matches
    def check_peek(self, kind):
        return kind == self.peek_token.kind

    # try to match. if not, error. Advances the current token
    def match(self, kind):
        if not self.check_token(kind):
            self.abort("Expected " + kind.name + " but found " + self.cur_token.kind.name)
        self.next()

    # advances current token
    def next(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.get_token()
        # lexer handles EOF

    def abort(self, msg):
        sys.exit("Parsing error. " + msg)
    
    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # since some nl's are required, we need to skip the excess
        while self.check_token(TokenType.NEWLINE):
            self.next()
        # parse all statements
        while not self.check_token(TokenType.EOF):
            self.statement()
    
    # 7 different types of statements
    def statement(self):
        # statement ::= "PRINT" (expression | string) nl
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next()

            if self.check_token(TokenType.STRING):
                # simple string
                self.next()
            else:
                # expect an expression
                self.expression()
        
        # "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()

            # parse all statements until ENDIF
            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        
        # "WHILE" comparison "REPEAT" nl {statement nl} "ENDWHILE" nl
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next()
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()

            # zero or more statements in the loop body
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)

        # "LABEL" ident nl
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next()
            # expect an identifier
            self.match(TokenType.IDENT)
        
        # "GOTO" ident nl
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next()
            # expect an identifier
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression nl
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next()
            # expect an identifier
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            # expect an expression
            self.expression()
        
        # "INPUT" ident nl
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next()
            # expect an identifier
            self.match(TokenType.IDENT)
        
        # error
        else:
            self.abort("Invalid statement of " + self.cur_token.text + " (" + self.cur_token.kind.name + ")")

        # newline
        self.nl()
    
    # nl ::= '\n' +
    def nl(self):
        print("NEWLINE")

        # require at least one newline
        self.match(TokenType.NEWLINE)
        # allow extra newlines
        while self.check_token(TokenType.NEWLINE):
            self.next()