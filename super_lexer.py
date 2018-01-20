import ply.lex as lex
from ply.lex import TOKEN
from super_assets import CompilationException, symbol_table
import copy

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
shenase = r'(\#(' + letter + r'{2})(' + digit + r'{3}))'
adadsabet = r'(' + digit + r'+)'
realconst = r'(' + digit + r'+)\.(' + digit + r'+)'
harf = r'((\'(.)\')|(\\(.)))'
boolsabet = r'((true)|(false))'
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


@TOKEN(realconst)
def t_REALCONST(t):
    t.value = {"value": float(t.value), "type": "float"}
    return t


@TOKEN(adadsabet)
def t_ADADSABET(t):
    t.value = {"value": int(t.value), "type": "int"}
    return t


@TOKEN(harf)
def t_HARF(t):
    if t.value == "\\0":
        t.value = {"value": 0, "type": "char"}
    elif t.value[0] == '\'':
        t.value = {"value": "\'" + t.value[1:len(t.value) - 1] + "\'", "type": "char"}
    else:
        t.value = {"value": "\'" + t.value[1:] + "\'", "type": "char"}
    return t


@TOKEN(boolsabet)
def t_BOOLSABET(t):
    if t.value == "true":
        value = 1
    else:
        value = 0
    t.value = {"value": value, "type": "bool"}
    return t


def t_COMMENTS(t):
    r'//.*'
    return


@TOKEN(reserved_wrd)
def t_RESERVED(t):
    if t.value in reserved:
        t.type = reserved[t.value]
        return t


@TOKEN(shenase)
def t_SHENASE(t):
    t.type = reserved.get(t.value, 'SHENASE')  # Check for reserved words
    # if t.type == "SHENASE":
        # if t.value in symbol_table:
        #     index = symbol_table.index(t.value)
        #     t.value = copy.deepcopy(symbol_table[index])
        # else:
        #     t.value = symbol_table.get_new_variable_dictionary(t.value)
    return t


def t_error(t):
    # raise CompilationException("Illegal character " + str(t.value[0]), t)
    # t.lexer.skip(1)
    print('lex error!')
    pass


# Build the lexer
lexer = lex.lex()

# # read input file
# input_code = open('./input.txt', 'r').read()
#
# # Give the lexer some input
# lexer.input(input_code)
#
# # write output
# output = ''
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok:
#         break  # No more input
#     output += str(tok) + '\n'
#
# # print(output)
#
# output_file = open('./output.txt', 'w')
# output_file.write(output)
