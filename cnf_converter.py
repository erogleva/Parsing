import re
import utils
from string import ascii_uppercase
from models import Rule


def _get_variables(rules):
    variables_set = set()
    for r in rules:
        # append the right hand side of every rule to the set of variables
        variables_set.add(r.LHS)
    return variables_set


def _get_terminals(rules):
    terminals_set = set()
    for r in rules:
        for symbol in r.RHS:
            if re.match(r"\'(.+)\'", symbol):
                terminals_set.add(symbol)
    return terminals_set


def _check_start_symbol_rhs(rules, start_symbol):
    for r in rules:
        if r.contains_start_symbol(start_symbol):
            return True


def _find_nullable_variable(rules):
    for r in rules:
        if r.is_epsilon_production():
            return r.LHS


def _eliminate_epsilon(rules, nullable_var):
    updated_rules = []
    for r in rules:
        if nullable_var in r.RHS:
            if len(r.RHS) == 1:
                # append epsilon rule if it was a unit production
                updated_rules = updated_rules + [Rule(r.LHS, ['/'])]
                updated_rules = updated_rules + [Rule(r.LHS, r.RHS)]
                continue
            else:
                # new combinations which omit every possible subset of the nullable variables
                new_rules = utils.create_combinations(r.RHS, nullable_var)
                for created_rule in new_rules:
                    updated_rules.append(Rule(r.LHS, created_rule))
                continue
        if r.LHS == nullable_var and r.RHS[0] == '/':
            # don't append the original epsilon rule
            continue
        else:
            # keep rule as it is
            updated_rules = updated_rules + [Rule(r.LHS, r.RHS)]
    return updated_rules


def _eliminate_recursive_units(rules):
    updated_rules = [x for x in rules if not x.is_recursive_unit()]
    return updated_rules


def _find_unit_production(rules, variables_set):
    for r in rules:
        if r.is_unit_production(variables_set):
            return r


def _find_long_production(rules):
    for r in rules:
        if r.has_long_production():
            return r


def _eliminate_unit_productions(rules, unit_prod):
    updated_rules = list(filter(lambda x: x.LHS != unit_prod.LHS or len(x.RHS) != 1 or x.RHS[0] != unit_prod.RHS[0], rules))
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
                if r.RHS[i] == new_rule.RHS[0] and r.RHS[i+1] == new_rule.RHS[1]:
                    new_prod = new_prod[:i] + [new_rule.LHS] + new_prod[i + 2:]
        updated_rules.append(Rule(r.LHS, new_prod))
    updated_rules.append(new_rule)
    return updated_rules


def convert_to_cnf(rules, start_symbol):
    production_rules = rules[:]
    variables = _get_variables(production_rules)
    available_vars = [x + '1' for x in ascii_uppercase if x != start_symbol] + [x for x in ascii_uppercase if
                                                                                x not in variables]
    terminals = _get_terminals(production_rules)

    # Eliminate start symbol on RHS

    if _check_start_symbol_rhs(production_rules, start_symbol):
        production_rules = [Rule(start_symbol + '1', [start_symbol])] + production_rules
        variables.add(start_symbol + '1')

    # Eliminate epsilon productions

    while True:
        nullable_variable = _find_nullable_variable(production_rules)
        if nullable_variable:
            production_rules = _eliminate_epsilon(production_rules, nullable_variable)
        else:
            break

    # Eliminate unit productions

    production_rules = _eliminate_recursive_units(production_rules)

    while True:
        unit_production = _find_unit_production(production_rules, variables)
        if unit_production:
            production_rules = _eliminate_unit_productions(production_rules, unit_production)
        else:
            break

    # Replace terminals in the right hand sides

    for terminal in terminals:
        if _check_if_terminal_needs_to_be_replaced(production_rules, terminal):
            new_rule = Rule(available_vars.pop(), [terminal])
            production_rules = _replace_terminals(production_rules, new_rule)

    # Replace long productions

    while True:
        long_production = _find_long_production(production_rules)
        if long_production:
            new_rule = Rule(available_vars.pop(), [long_production.RHS[0], long_production.RHS[1]])
            production_rules = _replace_long_productions(production_rules, new_rule)
        else:
            break

    return production_rules
