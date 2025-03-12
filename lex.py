import enum

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
        pass
    # skip whitespace except newlines, which will indicate end of statement
    def skip_whitespace(self):
        pass
    # skip comments
    def skip_comment(self):
        pass
    # return next token
    def get_token(self):
        if self.cur_char == '+':
            token = Token(self.cur_char, TokenType.PLUS)
        elif self.cur_char == '-':
            token = Token(self.cur_char, TokenType.MINUS)
        elif self.cur_char == '*':
            token = Token(self.cur_char, TokenType.ASTERISK)
        elif self.cur_char == '/':
            token = Token(self.cur_char, TokenType.SLASH)
        elif self.cur_char == '\n':
            token = Token(self.cur_char, TokenType.NEWLINE)
        elif self.cur_char == '\0':
            token = Token(self.cur_char, TokenType.EOF)
        else:
            # UNKNOWN
            pass
        self.next()
        return token

class Token:
    def __init__(self, text, kind):
        self.text = text # token actual text, used for strings and numbers
        self.kind = kind # token type that this token is classified as
    
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