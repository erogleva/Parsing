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