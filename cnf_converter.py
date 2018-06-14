from itertools import combinations
from string import ascii_uppercase
from classes import Rule, Grammar


def _check_start_symbol_rhs(rules, start_symbol):
    return next((r for r in rules if r.contains_start_symbol(start_symbol)), None)


def _find_nullable_variable(rules):
    return next((r.LHS for r in rules if r.is_epsilon_production()), None)


def _create_combinations(rule, unit):
    new_productions = []
    count = 0
    u_indexes = []
    number_to_remove = 1

    for index, symbol in enumerate(rule):
        if symbol == unit:
            u_indexes.append(index)
            count += 1

    for i in range(count, 0, -1):
        remove_indices = list(combinations(u_indexes, number_to_remove))
        for combo in remove_indices:
            new_rule = [j for k, j in enumerate(rule) if k not in combo]
            new_productions.append(new_rule)
        number_to_remove += 1

    new_productions.append(rule)
    return new_productions


def _eliminate_epsilon(rules, nullable_var):
    updated_rules = []
    for r in rules:
        if nullable_var in r.RHS:
            if len(r.RHS) == 1:
                # append epsilon rule if it was a unit production
                updated_rules = updated_rules + [Rule(r.LHS, ['/'])]
                updated_rules = updated_rules + [Rule(r.LHS, r.RHS)]
            else:
                # new combinations which omit every possible subset of the nullable variables
                new_rules = _create_combinations(r.RHS, nullable_var)
                for created_rule in new_rules:
                    updated_rules.append(Rule(r.LHS, created_rule))
        elif r.LHS == nullable_var and r.RHS[0] == '/':
            # don't append the original epsilon rule
            continue
        else:
            # keep rule as it is
            updated_rules = updated_rules + [Rule(r.LHS, r.RHS)]
    return updated_rules


def _eliminate_recursive_units(rules):
    updated_rules = [r for r in rules if not r.is_recursive_unit()]
    return updated_rules


def _find_unit_production(rules, variables_set):
    return next((r for r in rules if r.is_unit_production(variables_set)), None)


def _find_long_production(rules):
    return next((r for r in rules if r.has_long_production()), None)


def _eliminate_unit_productions(rules, unit_prod):
    updated_rules = list(
        filter(lambda x: x.LHS != unit_prod.LHS or len(x.RHS) != 1 or x.RHS[0] != unit_prod.RHS[0], rules))
    new_rules = [Rule(unit_prod.LHS, r.RHS) for r in rules if r.LHS == unit_prod.RHS[0]]
    updated_rules = updated_rules + new_rules
    return updated_rules


def _check_if_terminal_needs_to_be_replaced(rules, term):
    for r in rules:
        if term in r.RHS and len(r.RHS) > 1:
            return True


def _replace_terminals(rules, new_r):
    updated_rules = []
    for r in rules:
        if new_r.RHS[0] in r.RHS and len(r.RHS) > 1:
            productions = [new_r.LHS if x == new_r.RHS[0] else x for x in r.RHS]
            updated_rules.append(Rule(r.LHS, productions))
        else:
            updated_rules.append(Rule(r.LHS, r.RHS))
    updated_rules.append(new_r)
    return updated_rules


def _replace_long_productions(rules, new_rule):
    updated_rules = []
    for r in rules:
        new_prod = r.RHS[:]
        if len(new_prod) > 2:
            for i in range(len(r.RHS) - 1):
                if r.RHS[i] == new_rule.RHS[0] and r.RHS[i + 1] == new_rule.RHS[1]:
                    new_prod = new_prod[:i] + [new_rule.LHS] + new_prod[i + 2:]
        updated_rules.append(Rule(r.LHS, new_prod))
    updated_rules.append(new_rule)
    return updated_rules


def convert_to_cnf(rules, start_symbol):
    grammar = Grammar(start_symbol, rules)
    variables = grammar.variables
    available_vars = [x + '1' for x in ascii_uppercase if x != start_symbol] + [x for x in ascii_uppercase if
                                                                                x not in variables]
    terminals = grammar.terminals

    # Eliminate start symbol on RHS

    if _check_start_symbol_rhs(grammar.rules, start_symbol):
        grammar.rules = [Rule(start_symbol + '1', [start_symbol])] + grammar.rules
        grammar.start_symbol = start_symbol + '1'

    # Eliminate epsilon productions

    while True:
        nullable_variable = _find_nullable_variable(grammar.rules)
        if nullable_variable:
            grammar.rules = _eliminate_epsilon(grammar.rules, nullable_variable)
        else:
            break


    # Eliminate unit productions

    grammar.rules = _eliminate_recursive_units(grammar.rules)

    while True:
        unit_production = _find_unit_production(grammar.rules, variables)
        if unit_production:
            grammar.rules = _eliminate_unit_productions(grammar.rules, unit_production)
        else:
            break

    # Replace terminals in the right hand sides

    for terminal in terminals:
        if _check_if_terminal_needs_to_be_replaced(grammar.rules, terminal):
            new_rule = Rule(available_vars.pop(), [terminal])
            grammar.rules = _replace_terminals(grammar.rules, new_rule)

    # Replace long productions

    while True:
        long_production = _find_long_production(grammar.rules)
        if long_production:
            new_rule = Rule(available_vars.pop(), [long_production.RHS[0], long_production.RHS[1]])
            grammar.rules = _replace_long_productions(grammar.rules, new_rule)
        else:
            break

    return grammar.rules