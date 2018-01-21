import re
from tabulate import tabulate


class LR0er:
    def __init__(self, grammar):
        self.rules = None
        self.terminals = None
        self.non_terminals = None
        self.read_grammar(grammar)
        self.start_symbols = self.find_start_symbols()
        self.state_list = []
        self.build_state(rules=self.get_rules_for(self.start_symbols))
        print(self.get_table())

    def read_grammar(self, grammar):
        rules, t, therest = grammar.partition('Terminals:')
        terminals, nt, non_terminals = therest.partition('Non-Terminals:')
        self.terminals = set(filter(None, re.split(' |,', terminals.strip())))
        self.non_terminals = set(filter(None, re.split(' |,', non_terminals.strip())))
        self.rules = set()
        toks = list(sorted(self.terminals)) + list(sorted(self.non_terminals))
        for rule in rules.split('\n'):
            print(rule)
            rule = rule.strip()
            if rule == '' or rule is None:
                continue
            l, s, r = rule.partition('->')
            l = l.strip()
            r = r.strip()
            r_list = []
            while len(r) > 0:
                for tok in toks:
                    if r.startswith(tok):
                        r_list.append(tok)
                        r = r[len(tok):].strip()
                        break
            self.rules.add(Rule(l, r_list))

    def find_start_symbols(self):
        candidates = set(self.non_terminals)
        for rule in self.rules:
            for nt in self.non_terminals:
                if nt in rule.r and nt not in rule.l:
                    candidates.discard(nt)
        return candidates

    def get_rules_for(self, nt):
        if str(type(nt)) != '<class \'set\'>':
            nt_list = set()
            nt_list.add(nt)
        else:
            nt_list = nt
        rules = set()
        for rule in self.rules:
            if rule.l in nt_list:
                rules.add(rule)
        return rules

    def build_state(self, rules):
        s_index = len(self.state_list)
        # print(s_index, [str(r) for r in rules])
        s = State(s_index, self, rules)
        self.state_list.append(s)

        if s.handle:
            return

        # for each goto try to build a new state
        for tok, state_num in s.goto.items():
            next_rules = s.get_next_rules(tok)
            for st in self.state_list:
                if st.has_rules(next_rules):
                    s.goto[tok] = st.number
            if s.goto[tok] == -1:
                s.goto[tok] = len(self.state_list)
                self.build_state(next_rules)

    def get_table(self):
        cols = list(sorted(self.terminals)) + list(sorted(self.non_terminals))
        headers = ['State']
        for col in cols:
            headers.append(col)
        headers.append('Action')
        rows = []
        for st in self.state_list:
            row = ['S' + str(st.number)]
            for col in cols:
                if col in st.goto:
                    row.append(str(st.goto[col]))
                else:
                    row.append('-')
            row.append(st.action)
            rows.append(row)
        return tabulate(rows, headers)


class Rule:
    def __init__(self, l, r, pointer=0):
        self.l = l
        self.r = r
        self.pointer = pointer

    def __str__(self):
        r_str = ''
        for tok in self.r:
            r_str += tok
        return self.l + '->' + r_str

    def __copy__(self):
        return Rule(self.l, self.r.copy(), self.pointer)

    def __eq__(self, other):
        if str(self) == str(other) and self.pointer == other.pointer:
            return True
        return False

    def __hash__(self):
        return hash(str(self) + str(self.pointer))


class State:
    def __init__(self, number, lr0er, rules):
        self.number = number
        self.lr0er = lr0er
        self.rules = rules
        self.action = None
        self.handle = False
        self.goto = dict()
        self.expand_rules()

    def expand_rules(self):
        checked_rules = set()
        while True:
            new_rules = set()
            for rule in self.rules:
                if rule in checked_rules:
                    continue
                # if it's handle don't expand
                if rule.pointer == len(rule.r):
                    self.handle = True
                    print(str(self))
                    if rule.l in self.lr0er.start_symbols:
                        self.action = 'ACCEPT'
                    else:
                        self.action = 'reduce ' + str(rule)
                    return
                checked_rules.add(rule)

                current_tok = rule.r[rule.pointer]
                if current_tok in self.lr0er.non_terminals:  # if before non-terminal
                    # then expand
                    new_rules = new_rules | self.lr0er.get_rules_for(current_tok)
            self.rules = self.rules | new_rules

            if self.rules == checked_rules:
                break

        # initialise gotos
        for rule in self.rules:
            self.goto[rule.r[rule.pointer]] = -1

        self.action = 'shift'

        print(str(self))

    def __str__(self):
        st = 'S'+str(self.number) + '-----\n'
        for rule in self.rules:
            rule_str = rule.l + '->'
            for tok in rule.r[:rule.pointer]:
                rule_str += tok
            rule_str += '.'
            for tok in rule.r[rule.pointer:]:
                rule_str += tok
            st += rule_str + '\n'
        st += '-------\n'
        return st

    def has_rules(self, rules):
        for rule in rules:
            if rule not in self.rules:
                return False
        return True

    def get_next_rules(self, tok):
        next_rules = set()
        for rule in self.rules:
            if rule.r[rule.pointer] == tok:
                new_rule = rule.__copy__()
                new_rule.pointer += 1
                next_rules.add(new_rule)
        return next_rules


# smpl_grm = ["""S->aS
#               S->bA
#               S->cB
#               A->d
#               A->h
#               B->r
#               B->g
#
#               Terminals: a,b,c,d,h,r,g
#               Non-Terminals: S, A, B""",
#            """S->E
#               E->T;
#               E->T+E
#               T->int
#               T->(E)
#
#               Terminals: ; , (, ), int, +
#               Non-Terminals: S, E, T""",
#            """S->A
#               S->B
#               A->bA
#               A->d
#               B->aB
#               B->c
#
#               Terminals: a, b, d, c
#               Non-Terminals: S, A, B""",
#            """S->a
#               Terminals: a
#               Non-Terminals: S, E"""]
# aut = LR0er(smpl_grm[0])

# ./io/input_grammar.txt
path = input('grammar file path: ')
with open(str(path.strip()), 'r') as infile:
    grammar = infile.read()
aut = LR0er(str(grammar.strip()))

with open("./G_output.txt", 'w') as outfile:
    for st in aut.state_list:
        outfile.write(str(st)+'\n')
    outfile.write('\n'+aut.get_table())
