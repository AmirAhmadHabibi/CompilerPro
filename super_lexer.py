import ply.lex as lex
from ply.lex import TOKEN

# reserved words
reserved = {
    'program': 'PROGRAM',
    'main': 'MAIN',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'boolean': 'BOOLEAN',
    'ravie': 'RAVIE',
    'agar': 'AGAR',
    'angah': 'ANGAH',
    'vagarna': 'VAGARNA',
    'do': 'DO',
    'while': 'WHILE',
    'for': 'FOR',
    'gozinesh': 'GOZINESH',
    'end': 'END',
    'bazgasht': 'BAZGASHT',
    'exit': 'EXIT',
    'when': 'WHEN',
    'upto': 'UPTO',
    'downto': 'DOWNTO',
    'mored': 'MORED',
    'default': 'DEFAULT',
    'va': 'VA',
    'ya': 'YA',
    'naghiz': 'NAGHIZ'
}

# token names
tokens = ['SHENASE', 'ADADSABET', 'REALCONST', 'HARF', 'BOOLSABET', 'WHITESPACE', 'COMMENTS',
          'LT', 'LE', 'GT', 'GE', 'EQ', 'NEQ', 'LPAR', 'RPAR', 'LBRACK', 'RBRACK', 'LBRACE', 'RBRACE',
          'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'ASSIGNMENT_SIGN',
          'SEMICOLON', 'DOUBLE_DOT', 'COMMA', 'COLON'] + list(reserved.values())

letter = r'([a-zA-Z])'
digit = r'([0-9])'
reserved_wrd = r'(' + letter + r'+)'
t_SHENASE = r'(\#(' + letter + r'{2})(' + digit + r'{3}))'
t_ADADSABET = r'(' + digit + r'+)'
t_REALCONST = r'(' + digit + r'+)\.(' + digit + r'+)'
t_HARF = r'((\'(.)\')|(\\(.)))'
t_BOOLSABET = r'((true)|(false))'
whitespace = r'([ \t])+'
comments = r'//.*'

t_ignore = ' \t'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'='
t_NEQ = r'<>'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'\/'
t_MOD = r'\%'
t_ASSIGNMENT_SIGN = r'\:='
t_SEMICOLON = r';'
t_DOUBLE_DOT = r'\.\.'
t_COLON = r'\:'
t_COMMA = r'\,'


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return


def t_COMMENTS(t):
    r'//.*'
    return


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    # t.lexer.skip(1)


@TOKEN(reserved_wrd)
def t_RESERVED(t):
    if t.value in reserved:
        t.type = reserved[t.value]
        return t


# Build the lexer
lexer = lex.lex()

# read input file
input_code = open('./input.txt', 'r').read()

# Give the lexer some input
lexer.input(input_code)

output = ''
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    output += str(tok) + '\n'

# print(output)

output_file = open('./output.txt', 'w')
output_file.write(output)
