from itertools import combinations


def create_combinations(rule, unit):
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







