from classes import Backpointer, BinaryTree


def _find_substring_matches(table_cell, table, rules):
    # helper function for the construction of the CYK-chart:
    # finds all possible substring matches for a given cell in the chart
    # and stores a list of all the ways the corresponding node can be obtained as backpointers

    i, j = table_cell
    cell1_col = j - i - 1

    matches = {}

    for k in range(0, i + 1):
        cell2_row = i - k
        cell2_col = j - cell2_row

        for var1 in table[k][cell1_col]:
            for var2 in table[cell2_row][cell2_col]:
                combination = [var1, var2]
                for rule in rules:
                    if rule.RHS == combination:
                        if rule.LHS in matches:
                            matches[rule.LHS].append(Backpointer(rule, [k, cell1_col], [cell2_row, cell2_col]))
                        else:
                            matches[rule.LHS] = [Backpointer(rule, [k, cell1_col], [cell2_row, cell2_col])]

    return matches


def construct_cyk_chart(rules, string):
    # main function for the construction of the CYK-chart
    # in the 'first_row' considers all strings with length 1
    # for substrings of length 2 and greater, it considers every possible partition of the substring in two parts

    chart = []

    first_row = []
    for symbol in string:
        variables = [r.LHS for r in rules if r.RHS[0] == symbol]
        first_row.append(variables)
    chart.append(first_row)

    for j in range(1, len(string)):
        chart.append([])
        for i in range(0, j):
            chart[i + 1].append(_find_substring_matches([i, j], chart, rules))

    return chart


def print_parse_tree(tree, indent):
    if isinstance(tree, BinaryTree):
        tree_str = ' ' * indent + str(tree.data)
        if not isinstance(tree.left, BinaryTree):
            tree_str += '-->' + tree.left
        print(tree_str)
        indent = indent + 2
        print_parse_tree(tree.left, indent)
        print_parse_tree(tree.right, indent)


def _create_tree(data, cell, chart, string):
    tree = BinaryTree()
    tree.data = data

    if cell[0] != 0:
        bp = chart[cell[0]][cell[1]][data][0] # TODO
        tree.left = _create_tree(bp.rule.RHS[0], bp.cell1, chart, string)
        tree.right = _create_tree(bp.rule.RHS[1], bp.cell2, chart, string)
    else:
        tree.left = string[cell[1]]

    return tree


def parse(chart, string):
    parse_tree = _create_tree('S', [len(chart) - 1, 0], chart, string)
    print_parse_tree(parse_tree, 0)
    return parse_tree

