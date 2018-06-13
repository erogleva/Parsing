from Node import Backpointer
from BinaryTree import Tree

def create_rule_combinations(table_cell, table, rules):
    i, j = table_cell
    col = j - i - 1
    number_of_combinations = i + 1
    combinations = {}

    for k in range(0, number_of_combinations):
        cell1 = table[k][col]
        cell2_row = number_of_combinations - k - 1
        cell2 = table[cell2_row][j - cell2_row]
        for var1 in cell1:
            for var2 in cell2:
                combo = [var1, var2]
                for rule in rules:
                    if rule.RHS == combo:
                        if rule.LHS in combinations:
                            combinations[rule.LHS].append(Backpointer(rule, [k, col], [cell2_row, j - cell2_row]))
                        else:
                            combinations[rule.LHS] = [Backpointer(rule, [k, col], [cell2_row, j - cell2_row])]

    return combinations


def construct_cyk_chart(rules, input_string):
    table = []
    string = input_string.split()
    # strings length 1:

    first_row = []
    for symbol in string:
        variables = [r.LHS for r in rules if r.RHS[0] == symbol]
        first_row.append(variables)

    table.append(first_row)

    for j in range(1, len(string)):
        table.append([])
        for i in range(0, j):
            table[i + 1].append(create_rule_combinations([i, j], table, rules))

    return table


def parse(chart):
    parse_tree = Tree()

    bp = chart[len(chart) - 1][0]['S'][1]
    parse_tree.data = bp.rule.LHS
    parse_tree.left = create_tree(bp.rule.RHS[0], bp.cell1, chart)
    parse_tree.right = create_tree(bp.rule.RHS[1], bp.cell2, chart)

    return parse_tree


def create_tree(data, cell, chart):
    tree = Tree()
    tree.data = data

    if cell[0] != 0:
        bp = chart[cell[0]][cell[1]][data][0]
        tree.left = create_tree(bp.rule.RHS[0], bp.cell1, chart)
        tree.right = create_tree(bp.rule.RHS[1], bp.cell2, chart)

    return tree