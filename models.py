import re


class Rule:
    def __init__(self, lhs, rhs):
        self.LHS = lhs  # string
        self.RHS = rhs  # list

    def is_epsilon_production(self):
        return self.RHS == ['/']

    def contains_start_symbol(self, start_symbol):
        return start_symbol in self.RHS

    def is_unit_production(self, variables):
        return len(self.RHS) == 1 and self.RHS[0] in variables

    def has_long_production(self):
        return len(self.RHS) > 2

    def is_recursive_unit(self):
        return self.LHS == self.RHS[0] and len(self.RHS) == 1


class Grammar:
    def __init__(self, start_symbol, rules):
        self._start_symbol = start_symbol
        self._rules = rules

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    @property
    def start_symbol(self):
        return self._start_symbol

    @start_symbol.setter
    def start_symbol(self, value):
        self._start_symbol = value

    @property
    def variables(self):
        return {r.LHS for r in self._rules}

    @property
    def terminals(self):
        terminals_set = set()
        for r in self._rules:
            for symbol in r.RHS:
                if re.match(r"\'(.+)\'", symbol):
                    terminals_set.add(symbol)
        return terminals_set

    def print_rules(self):
        for r in self._rules:
            print(r.LHS + ' -> ' + ' '.join(r.RHS))