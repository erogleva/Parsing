def combine(rule1, rule2, allrules):
    solutions = set()
    for var1 in rule1:
        for var2 in rule2:
            combo = [var1, var2]
            for rule in allrules:
                if rule.RHS == combo:
                    solutions.add(rule.LHS)
    return solutions


def create_rule_combinations(table_cell, table, rules):
    i, j = table_cell
    col = j - i - 1
    number_of_combinations = i + 1
    combinations = set()

    for k in range(0, number_of_combinations):
        cell1 = table[k][col]
        cell2_row = number_of_combinations - k - 1
        cell2 = table[cell2_row][j - cell2_row]
        solutions = combine(cell1, cell2, rules)
        for solution in solutions:
            combinations.add(solution)

    return combinations


def construct_cyk_chart(rules, input_string):
    table = []
    string = input_string.split()
    # strings length 1:

    first_row = []
    for symbol in string:
        variables = {r.LHS for r in rules if r.RHS[0] == symbol}
        first_row.append(variables)

    table.append(first_row)

    for j in range(1, len(string)):
        table.append([])
        for i in range(0, j):
            table[i + 1].append(create_rule_combinations([i, j], table, rules))

    for j in table:
        print(j)
