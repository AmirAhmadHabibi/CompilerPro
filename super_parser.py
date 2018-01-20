import ply.yacc as yacc
from super_lexer import tokens, lexer

start = 'program'

precedence = (
    ('right', 'ANGAH', 'VAGARNA'),
)


def p_program(p):
    """program      : PROGRAM SHENASE declarations_list list_ravie MAIN block
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
    """declarator_list      : declarator
                            | declarator_list COMMA declarator"""


def p_declarator(p):
    """declarator       : dec
                        | dec ASSIGNMENT_SIGN meghdar_avalie"""


def p_dec(p):
    """dec      : SHENASE
                | SHENASE LBRACK range RBRACK
                | SHENASE LBRACK ADADSABET RBRACK"""


def p_range(p):
    """range        : SHENASE DOUBLE_DOT SHENASE
                    | ADADSABET DOUBLE_DOT ADADSABET
                    | ebarat_riazi DOUBLE_DOT ebarat_riazi"""


def p_meghdar_avalie(p):
    """meghdar_avalie      : ebarat_sabet
                        | LBRACE list_meghdar_avalie RBRACE"""


def p_list_meghdar_avalie(p):
    """list_meghdar_avalie      : ebarat_sabet COMMA list_meghdar_avalie
                                | ebarat_sabet"""


def p_list_ravie(p):
    """list_ravie       : list_ravie ravie
                        | ravie"""


def p_ravie(p):
    """ravie        : RAVIE SHENASE parameters LBRACE declarations_list block RBRACE SEMICOLON
                    | RAVIE SHENASE parameters LBRACE block RBRACE SEMICOLON"""


def p_parameters(p):
    """parameters       : LPAR declarations_list RPAR
                        | LPAR RPAR"""


def p_block(p):
    """block        : LBRACE statement_list RBRACE"""


def p_statement_list(p):
    """statement_list       : statement SEMICOLON
                            | statement_list statement SEMICOLON"""


def p_statement_assignment(p):
    """statement            : SHENASE ASSIGNMENT_SIGN ebarat
                            | SHENASE LBRACK ebarat RBRACK ASSIGNMENT_SIGN ebarat"""


def p_statement_function_call(p):
    """statement            : SHENASE LPAR arguments_list RPAR"""


def p_statement_function_return(p):
    """statement            : BAZGASHT ebarat"""


def p_statement_if(p):
    """statement            : AGAR ebarat_bool ANGAH statement
                            | AGAR ebarat_bool ANGAH statement VAGARNA statement"""


def p_statement_do_while(p):
    """statement            : DO statement WHILE ebarat_bool"""


def p_statement_for(p):
    """statement            : FOR SHENASE ASSIGNMENT_SIGN counter DO statement"""


def p_statement_switch(p):
    """statement            : GOZINESH ebarat onsor_mored default END"""


def p_statement_exit_when(p):
    """statement            : EXIT WHEN ebarat_bool"""


def p_statement_block(p):
    """statement            : block
                            | """


def p_arguments_list(p):
    """arguments_list       : multi_arguments
                            | """


def p_multi_arguments(p):
    """multi_arguments      : multi_arguments COMMA ebarat
                            | ebarat"""


def p_counter(p):
    """counter      : ADADSABET UPTO ADADSABET
                    | ADADSABET DOWNTO ADADSABET"""


def p_onsor_mored(p):
    """onsor_mored     : MORED ADADSABET COLON block
                        | onsor_mored MORED ADADSABET COLON block"""


def p_default(p):
    """default      : DEFAULT COLON block"""


def p_ebarat(p):
    """ebarat      : ebarat_sabet
                    | ebarat_bool
                    | ebarat_riazi
                    | SHENASE
                    | SHENASE LBRACK ebarat RBRACK
                    | LPAR ebarat RPAR"""


def p_ebarat_function_call(p):
    """ebarat      : SHENASE LPAR arguments_list RPAR"""


def p_ebarat_sabet(p):
    """ebarat_sabet     : ADADSABET
                        | REALCONST
                        | HARF
                        | BOOLSABET"""


def p_ebarat_bool_comparator(p):
    """ebarat_bool      : zojmoratab LT
                        | zojmoratab LE
                        | zojmoratab GT
                        | zojmoratab GE
                        | zojmoratab EQ
                        | zojmoratab NEQ"""


def p_ebarat_bool_and(p):
    """ebarat_bool     : zojmoratab VA"""


def p_ebarat_bool_or(p):
    """ebarat_bool     : zojmoratab YA"""


def p_ebarat_bool_and_then(p):
    """ebarat_bool     : VA ANGAH zojmoratab"""


def p_ebarat_bool_or_else(p):
    """ebarat_bool     : YA VAGARNA zojmoratab"""


def p_ebarat_bool_not(p):
    """ebarat_bool     : ebarat NAGHIZ"""


def p_ebarat_riazi(p):
    """ebarat_riazi         : zojmoratab PLUS
                            | zojmoratab MINUS
                            | zojmoratab MULT
                            | zojmoratab DIV
                            | zojmoratab MOD
                            | ebarat MINUS"""


def p_zojmoratab(p):
    """zojmoratab     : LPAR ebarat COMMA ebarat RPAR"""


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
