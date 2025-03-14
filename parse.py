import sys
from lex import *

# Parser class
# object keeps track of the current token and checks if the code matches the grammar
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set() # variables declared
        self.labels_declared = set() # labels declared
        self.labels_gotoed = set() # labels goto'ed

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
        # start of program
        self.emitter.header_line("#include <iostream>")
        self.emitter.header_line("using namespace std;")
        self.emitter.header_line("int main() {")

        # since some nl's are required, we need to skip the excess
        while self.check_token(TokenType.NEWLINE):
            self.next()
        # parse all statements
        while not self.check_token(TokenType.EOF):
            self.statement()
        
        # end of program
        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

        # check that label referenced in GOTO is declared
        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort("Attempting to GOTO to undeclared label: " + label)
    
    # 7 different types of statements
    def statement(self):
        # statement ::= "PRINT" (expression | string) nl
        if self.check_token(TokenType.PRINT):
            self.next()

            if self.check_token(TokenType.STRING):
                # simple string
                self.emitter.emit_line("cout << \"" + self.cur_token.text + "\\n\";")
                self.next()
            else:
                # expect an expression
                self.emitter.emit("cout << ")
                self.expression()
                self.emitter.emit_line(";")
        
        # "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.check_token(TokenType.IF):
            self.next()
            self.emitter.emit_line("if (")
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emit_line(") {")

            # parse all statements until ENDIF
            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")
        
        # "WHILE" comparison "REPEAT" nl {statement nl} "ENDWHILE" nl
        elif self.check_token(TokenType.WHILE):
            self.next()
            self.emitter.emit("while (")
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emit_line(") {")

            # zero or more statements in the loop body
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")

        # "LABEL" ident nl
        elif self.check_token(TokenType.LABEL):
            self.next()

            # check if label doesnt already exist
            if self.cur_token.text in self.labels_declared:
                self.abort("Label already exists: " + self.cur_token.text)
            self.labels_declared.add(self.cur_token.text)
            self.emitter.emit_line(self.cur_token.text + ":")

            # expect an identifier
            self.match(TokenType.IDENT)
        
        # "GOTO" ident nl
        elif self.check_token(TokenType.GOTO):
            self.next()
            # dont need to check if it already exists because we can go to the label multiple times
            self.labels_gotoed.add(self.cur_token.text)
            self.emitter.emit_line("goto " + self.cur_token.text + ";")
            # expect an identifier
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression nl
        elif self.check_token(TokenType.LET):
            self.next()

            # check if variable already exists
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.emit_line("double " + self.cur_token.text + ";")

            # expect an identifier
            self.emitter.emit(self.cur_token.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            # expect an expression
            self.expression()
            self.emitter.emit_line(";")
        
        # "INPUT" ident nl
        elif self.check_token(TokenType.INPUT):
            self.next()

            # check if variable already exists
            if self.cur_token.text not in self.symbols:
                self.symbols.add(self.cur_token.text)
                self.emitter.emit_line("double " + self.cur_token.text + ";")

            self.emitter.emit_line("cin >> " + self.cur_token.text + ";")
            # expect an identifier
            self.match(TokenType.IDENT)
        
        # error
        else:
            self.abort("Invalid statement of " + self.cur_token.text + " (" + self.cur_token.kind.name + ")")

        # newline
        self.nl()
    
    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        # expect an expression
        self.expression()
        # must be at least one comparison operator
        if self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            self.next()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.cur_token.text)
        
        while self.is_comparison_operator():
            self.emitter.emit(self.cur_token.text)
            # allow multiple comparison operators
            self.next()
            # expect an expression
            self.expression()
    
    # expression ::= term {("+" | "-") term}
    def expression(self):
        # expect a term
        self.term()
        # can have zero or more +/- and expressions
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next()
            self.term()
    
    # term :: unary {( "/" | "*" ) unary}
    # have precedence over +-
    def term(self):
        # expect a unary
        self.unary()
        # can have zero or more * / and unary
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.emitter.emit(self.cur_token.text)
            self.next()
            self.unary()
    
    # unary :: [ "+" | "-" ] primary
    def unary(self):
        # optional sign
        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.cur_token.text)
            self.next()
        # expect a primary
        self.primary()
    
    # primary ::= number | ident
    def primary(self):
        # expect a number or identifier
        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.cur_token.text)
            self.next()
        elif self.check_token(TokenType.IDENT):
            # check if variable exists
            if self.cur_token.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.cur_token.text)
            self.emitter.emit(self.cur_token.text)
            self.next()
        else:
            self.abort("Unexpected token at " + self.cur_token.text)
    
    def is_comparison_operator(self):
        return self.check_token(TokenType.EQ) or self.check_token(TokenType.NOTEQ) or \
            self.check_token(TokenType.GT) or self.check_token(TokenType.GTEQ) or \
            self.check_token(TokenType.LT) or self.check_token(TokenType.LTEQ)

    # nl ::= '\n' +
    def nl(self):
        # require at least one newline
        self.match(TokenType.NEWLINE)
        # allow extra newlines
        while self.check_token(TokenType.NEWLINE):
            self.next()