import ply.yacc as yacc
from super_lexer import tokens, lexer

start = 'program'

precedence = (
    ('right', 'ANGAH', 'VAGARNA'),
)


def p_program(p):
    """program          : PROGRAM SHENASE declarations_list list_ravie MAIN block
                        | PROGRAM SHENASE list_ravie MAIN block
                        | PROGRAM SHENASE declarations_list MAIN block
                        | PROGRAM SHENASE MAIN block"""


def p_declarations_list(p):
    """declarations_list    : declarations
                            | declarations_list declarations"""


def p_declarations(p):
    """declarations     : taeen_type declarator_list SEMICOLON"""


def p_taeen_type(p):
    """taeen_type       : INT
                        | FLOAT
                        | CHAR
                        | BOOLEAN"""


def p_declarator_list(p):
    """declarator_list  : declarator
                        | declarator_list COMMA declarator"""


def p_declarator(p):
    """declarator       : dec
                        | dec ASSIGNMENT_SIGN meghdar_avalie"""


def p_dec(p):
    """dec              : SHENASE
                        | SHENASE LBRACK range RBRACK
                        | SHENASE LBRACK ADADSABET RBRACK"""


def p_range(p):
    """range            : SHENASE DOUBLE_DOT SHENASE
                        | ADADSABET DOUBLE_DOT ADADSABET
                        | ebarat_riazi DOUBLE_DOT ebarat_riazi"""


def p_meghdar_avalie(p):
    """meghdar_avalie   : ebarat_sabet
                        | LBRACE list_meghdar_avalie RBRACE"""


def p_list_meghdar_avalie(p):
    """list_meghdar_avalie      : ebarat_sabet COMMA list_meghdar_avalie
                                | ebarat_sabet"""


def p_list_ravie(p):
    """list_ravie       : list_ravie ravie
                        | ravie"""


def p_ravie(p):
    """ravie            : RAVIE SHENASE parameters LBRACE declarations_list block RBRACE SEMICOLON
                        | RAVIE SHENASE parameters LBRACE block RBRACE SEMICOLON"""


def p_parameters(p):
    """parameters       : LPAR declarations_list RPAR
                        | LPAR RPAR"""


def p_block(p):
    """block            : LBRACE statement_list RBRACE"""


def p_statement_list(p):
    """statement_list   : statement SEMICOLON
                        | statement_list statement SEMICOLON"""


def p_statement(p):
    """statement        : SHENASE ASSIGNMENT_SIGN ebarat
                        | AGAR ebarat_bool ANGAH statement
                        | AGAR ebarat_bool ANGAH statement VAGARNA statement
                        | DO statement WHILE ebarat_bool
                        | FOR SHENASE ASSIGNMENT_SIGN counter DO statement
                        | GOZINESH ebarat onsor_mored default END
                        | SHENASE LPAR arguments_list RPAR
                        | SHENASE LBRACK ebarat RBRACK ASSIGNMENT_SIGN ebarat
                        | BAZGASHT ebarat
                        | EXIT WHEN ebarat_bool
                        | block
                        | """


def p_arguments_list(p):
    """arguments_list   : multi_arguments
                        | """


def p_multi_arguments(p):
    """multi_arguments  : multi_arguments COMMA ebarat
                        | ebarat"""


def p_counter(p):
    """counter          : ADADSABET UPTO ADADSABET
                        | ADADSABET DOWNTO ADADSABET"""


def p_onsor_mored(p):
    """onsor_mored      : MORED ADADSABET COLON block
                        | onsor_mored MORED ADADSABET COLON block"""


def p_default(p):
    """default          : DEFAULT COLON block
                        |"""


def p_ebarat(p):
    """ebarat           : ebarat_sabet
                        | ebarat_bool
                        | ebarat_riazi
                        | SHENASE
                        | SHENASE LBRACK ebarat RBRACK
                        | SHENASE LPAR arguments_list RPAR
                        | LPAR ebarat RPAR"""


def p_ebarat_sabet(p):
    """ebarat_sabet     : ADADSABET
                        | REALCONST
                        | HARF
                        | BOOLSABET"""


def p_ebarat_bool(p):
    """ebarat_bool      : zojmoratab VA
                        | zojmoratab YA
                        | VA ANGAH zojmoratab
                        | YA VAGARNA zojmoratab
                        | zojmoratab LT
                        | zojmoratab LE
                        | zojmoratab GT
                        | zojmoratab GE
                        | zojmoratab EQ
                        | zojmoratab NEQ
                        | ebarat NAGHIZ"""


def p_ebarat_riazi(p):
    """ebarat_riazi     : zojmoratab PLUS
                        | zojmoratab MINUS
                        | zojmoratab MULT
                        | zojmoratab DIV
                        | zojmoratab MOD
                        | ebarat MINUS"""


def p_zojmoratab(p):
    """zojmoratab       : LPAR ebarat COMMA ebarat RPAR"""


def p_error(p):
    msg = "Syntax error in input!\n" + str(p)
    print(msg)


# yacc.yacc(method='LALR', tabmodule="parsing_table")

try:
    parser = yacc.yacc(method='LALR', tabmodule="parsing_table")
    with open("./io/input.txt", 'r') as input_file:
        code = input_file.read()
    parser.parse(code, lexer=lexer, debug=False, tracking=True)
    print("Parsed with no errors")
except Exception as e:
    print(e)
