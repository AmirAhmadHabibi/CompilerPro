import re


class LR0er:
    def __init__(self, grammar):
        self.rules = None
        self.terminals = None
        self.non_terminals = None
        self.read_grammar(grammar)
        self.start_symbols = self.find_start_symbols()
        self.state_list = []
        self.build_state(rules=self.get_rules_for(self.start_symbols))
        self.print_table()

    def read_grammar(self, grammar):
        rules, t, therest = grammar.partition('Terminals:')
        self.rules = set([Rule(rl) for rl in rules.split()])
        terminals, nt, non_terminals = therest.partition('Non-Terminals:')
        self.terminals = set(filter(None, re.split(' |,', terminals.strip())))
        self.non_terminals = set(filter(None, re.split(' |,', non_terminals.strip())))

    def find_start_symbols(self):
        candidates = set(self.non_terminals)
        for rule in self.rules:
            for nt in self.non_terminals:
                if nt in rule.r and nt not in rule.l:
                    candidates.remove(nt)
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

    def print_table(self):
        cols = list(self.terminals) + list(self.non_terminals)
        table = '__'
        for col in cols:
            table += '\t\t' + col
        table += '\t\tAction\n'
        for st in self.state_list:
            table += 'S' + str(st.number)
            for col in cols:
                if col in st.goto:
                    table += '\t\t' + str(st.goto[col])
                else:
                    table += '\t\t_'
            table += '\t\t' + st.action + '\n'
        print(table)


class Rule:
    def __init__(self, rl, pointer=0):
        self.l, s, self.r = rl.partition('->')
        self.pointer = pointer

    def __str__(self):
        return self.l + '->' + self.r

    def __copy__(self):
        return Rule(self.__str__(), self.pointer)

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
                    self.print()
                    # set action
                    self.action = 'reduce ' + str(rule)
                    return
                checked_rules.add(rule)

                current_tok = rule.r[rule.pointer]
                if current_tok in self.lr0er.non_terminals:
                    # then expand
                    new_rules = new_rules | self.lr0er.get_rules_for(current_tok)
            self.rules = self.rules | new_rules

            if self.rules == checked_rules:
                break

        # initialise gotos
        for rule in self.rules:
            self.goto[rule.r[rule.pointer]] = -1

        # set action
        self.action = 'shift'

        # print the state
        self.print()

    def print(self):
        print(self.number, '-----')
        for rule in self.rules:
            r = str(rule.r) + ' '
            print(rule.l + '->' + r[:rule.pointer] + '.' + r[rule.pointer:])
        print('-------\n')

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


str_grm = """S->aS
            S->bA
            S->cB
            A->d
            A->h
            B->r
            B->g
            
            Terminals: a,b,c,d,h,r,g
            Non-Terminals: S, A, B"""
aut = LR0er(str_grm)
# print([str(r) for r in aut.rules])
