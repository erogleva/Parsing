from cnf_converter import convert_to_cnf
from common import Rule
from cyk_chart import CYK_Parser
import re


def preprocess_rules(rules):
    # split left and right hand sides
    updated = [r.split('->') for r in rules if r != '']
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


def strip_quotation_marks(rules):
    updated_rules = []
    for r in rules:
        terminal = re.match(r"\'(.+)\'", r.RHS[0])
        if terminal:
            updated_rules.append(Rule(r.LHS, [terminal.group(1)]))
        else:
            updated_rules.append(r)
    return updated_rules


# MAIN
if __name__ == "__main__":
    source = open('./test_grammars/grammar.txt').readlines()
    initial_rules = [line.strip() for line in source]

    start_symbol = initial_rules.pop(0)
    production_rules = preprocess_rules(initial_rules)

    grammar = convert_to_cnf(production_rules, start_symbol)
    grammar.rules = strip_quotation_marks(grammar.rules)
    grammar.print_rules()

    parser = CYK_Parser('I shot an elephant in my pajamas'.split(), grammar)

    if parser.accepted:
        print('String was accepted by the grammar')
        parser.parse()
    else:
        print('String was rejected')