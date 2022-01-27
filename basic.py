# digets 

from turtle import left, right


DIGITS = '0123456789'


#errors 
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        res = f'{self.error_name}: {self.details}'
        res += f'File {self.pos_start.fn}, line{self.pos_start.ln +1}'
        return res
    
class IllegalCharError(Error):
    def __init__(self,pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character (you got this, you can fix the problem)', details)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '/n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln , self.col, self.fn, self.ftxt)
    

# tokens 


TT_INT  = 'TT_INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LP = 'LP'
TT_RP = 'RP'



class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: 
            return f'{self.type}:{self.value}'
        return f'{self.type}'

# lexer

class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.fn = fn
        self.pos = Position(-1, 0 , -1,fn, text )
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number()) 
            elif self.current_char =='+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LP))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RP))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + "." :
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str +="."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
            
  
 # NODES

class numberNode:
    def __init__(self, tok):
        self.tok = tok
    def __repr__(self):
        return f'{slef.tok}'




class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
# parser 
class Parser:
    def __init__(self, tokens): #  I MADE THE EXECUTIVE DESISHION TO ADD SELF 
        self.tokens = tokens
        self.tok_idx = 1
        self.advance()

    def advance():
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    # make the expr/term/factor from sintax.txt 



# run 

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
