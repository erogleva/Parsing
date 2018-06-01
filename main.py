from cnf_converter import convert_to_cnf
from models import Rule


def preprocess_rules(rules):
    # split left and right hand sides
    updated = [r.split('->') for r in rules]
    # strip unnecessary spaces
    updated = [[x.strip() for x in r] for r in updated]

    result = []
    # split rules with multiple productions into simpler ones & append to result
    for r in updated:
        if '|' in r[1]:
            productions = r[1].split('|')
            for prod in productions:
                result.append(Rule(r[0], prod.split()))
        else:
            result.append(Rule(r[0], r[1].split()))
    return result


def print_rules(rules):
    for r in rules:
        print(r.LHS + ' -> ' + ' '.join(r.RHS))


# MAIN
source = open('grammar5.txt').readlines()
initial_rules = [line.strip() for line in source]

start_symbol = initial_rules.pop(0)
production_rules = preprocess_rules(initial_rules)

production_rules = convert_to_cnf(production_rules, start_symbol)
print_rules(production_rules)
