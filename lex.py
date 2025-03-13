import enum
import sys

# lexer
class Lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.cur_char = '' # current character in string
        self.cur_pos = -1 # current position in string
        self.next()
    # process next char
    def next(self):
        self.cur_pos += 1
        # if at end of input
        if self.cur_pos >= len(self.source):
            self.cur_char = '\0' # EOF
        else:
            self.cur_char = self.source[self.cur_pos]
    # return the lookahead char
    def peek(self):
        # if next is at end of input
        if self.cur_pos + 1 >= len(self.source):
            return '\0' # EOF
        return self.source[self.cur_pos + 1]
    # inavlid token
    def abort(self, msg):
        sys.exit("Lexing error. " + msg)
    # skip whitespace except newlines, which will indicate end of statement
    def skip_whitespace(self):
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\r':
            self.next()
    # skip comments
    def skip_comment(self):
        if self.cur_char == '#':
            while self.cur_char != '\n':
                self.next()
    # return next token
    def get_token(self):
        self.skip_whitespace()
        self.skip_comment()
        token = None
        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == '=':
            # check for EQ or EQEQ
            if self.peek() == '=':
                last_char = self.cur_char
                self.next()
                token = Token(last_char + self.cur_char, TokenType.EQEQ)
            else:
                token = Token(self.cur_char, TokenType.EQ)
        elif self.cur_char == '>':
            # check for GTEQ
            if self.peek() == '=':
                last_char = self.cur_char
                self.next()
                token = Token(last_char + self.cur_char, TokenType.GTEQ)
            else:
                token = Token(self.cur_char, TokenType.GT)
        elif self.cur_char == '<':
            # check for LTEQ
            if self.peek() == '=':
                last_char = self.cur_char
                self.next()
                token = Token(last_char + self.cur_char, TokenType.LTEQ)
            else:
                token = Token(self.cur_char, TokenType.LT)
        elif self.cur_char == '!':
            # check for NOTEQ
            if self.peek() == '=':
                last_char = self.cur_char
                self.next()
                token = Token(last_char + self.cur_char, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.cur_char == '\"':
            # string literal
            self.next()
            start_pos = self.cur_pos
            while self.cur_char != '\"':
                if self.cur_char == '\r' or self.cur_char == '\n' or self.cur_char == '\t' or self.cur_char == '\\' or self.cur_char == '%':
                    self.abort("Illegal character in string literal")
                self.next()
            token_text = self.source[start_pos:self.cur_pos] # get string literal from start pos to current pos
            token = Token(token_text, TokenType.STRING)
        elif self.cur_char.isdigit():
            # leading char is a digit
            # get all consecutive digits and decimal if there is one
            start_pos = self.cur_pos
            while self.peek().isdigit():
                self.next()
            if self.peek() == '.':
                self.next()
                # must have at least one digit after decimal
                if not self.peek().isdigit():
                    # error
                    self.abort("Illegal character in number literal")
                while self.peek().isdigit():
                    self.next()
            token_text = self.source[start_pos:self.cur_pos + 1] # get number literal from start pos to current pos
            token = Token(token_text, TokenType.NUMBER)
        elif self.cur_char.isalpha():
            # leading char is a letter
            # get all consecutive letters
            start_pos = self.cur_pos
            while self.peek().isalnum():
                self.next()
            
            # check for keywords
            token_text = self.source[start_pos:self.cur_pos + 1] # get identifier from start pos to current pos
            keyword = Token.checkKeyword(token_text)
            if keyword is not None:
                token = Token(token_text, keyword)
            else:
                token = Token(token_text, TokenType.IDENT)

        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token(self.cur_char, TokenType.EOF)
        else:
            # UNKNOWN
            self.abort("Unknown token: " + self.cur_char)
        self.next()
        return token

class Token:
    def __init__(self, text, kind):
        self.text = text # token actual text, used for strings and numbers
        self.kind = kind # token type that this token is classified as
    
    @staticmethod
    def checkKeyword(text):
        for kind in TokenType:
            # relies on all keywords eval #'s being 1XX
            if kind.name == text and kind.value >= 100 and kind.value < 200:
                    return kind
        # didn't find keyword
        return None
    
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211