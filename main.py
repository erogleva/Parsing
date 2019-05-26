from cnf_converter import convert_to_cnf
from common import Rule
from cyk_parser import CYK_Parser
import re
import sys


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
    source = open(sys.argv[1]).readlines()
    sentences = open(sys.argv[2]).readlines()
    initial_rules = [line.strip() for line in source]
    sentences = [line.strip() for line in sentences]

    start_symbol = initial_rules.pop(0)
    production_rules = preprocess_rules(initial_rules)

    grammar = convert_to_cnf(production_rules, start_symbol)
    grammar.rules = strip_quotation_marks(grammar.rules)

    print('Rules after CNF conversion:')
    grammar.print_rules()
    print()

    for sent in sentences:
        parser = CYK_Parser(sent.split(), grammar)
        if parser.accepted:
            print(sent + ': Accepted by the grammar')
            print('Parse tree(s)')
            parser.parse()
        else:
            print(sent + ': Rejected by the grammar')