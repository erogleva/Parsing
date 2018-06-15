class BinaryTree:
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data


class Backpointer:
    def __init__(self, rule, cell1, cell2):
        self.rule = rule
        self.cell1 = cell1
        self.cell2 = cell2


class CYK_Parser:
    def __init__(self, string, grammar):
        self.possible_trees = 1
        self.string = string
        self.grammar = grammar
        self.accepted = False
        self.chart = self.constuct_cyk_chart()
        self.curr_variable = ''
        self.position = None

    @staticmethod
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


    def constuct_cyk_chart(self):
        # main function for the construction of the CYK-chart
        # in the 'first_row' considers all strings with length 1
        # for substrings of length 2 and greater, it considers every possible partition of the substring in two parts
        chart = []
        first_row = []
        for symbol in self.string:
            variables = [r.LHS for r in self.grammar.rules if r.RHS[0] == symbol]
            first_row.append(variables)
        chart.append(first_row)

        for j in range(1, len(self.string)):
            chart.append([])
            for i in range(0, j):
                chart[i + 1].append(self._find_substring_matches([i, j], chart, self.grammar.rules))

        if self.grammar.start_symbol in chart[len(chart) - 1][0].keys():
            print(chart[len(chart) - 1][0])
            print(list(chart[len(chart) - 1][0].keys()))
            print(str(self.grammar.start_symbol))
            self.accepted = True

        return chart

    def _create_tree(self, variable, cell, num):
        tree = BinaryTree()
        tree.data = variable

        if cell[0] != 0:
            if len(self.chart[cell[0]][cell[1]][variable]) > 1:
                self.possible_trees = len(self.chart[cell[0]][cell[1]][variable])
                self.curr_variable = variable
                self.position = [cell[0], cell[1]]
            if variable == self.curr_variable and [cell[0], cell[1]] == self.position:
                backpointer = self.chart[cell[0]][cell[1]][variable][num]
            else:
                backpointer = self.chart[cell[0]][cell[1]][variable][0]
            tree.left = self._create_tree(backpointer.rule.RHS[0], backpointer.cell1, num)
            tree.right = self._create_tree(backpointer.rule.RHS[1], backpointer.cell2, num)
        else:
            tree.left = self.string[cell[1]]

        return tree

    def print_parse_tree(self, tree, indent):
        if isinstance(tree, BinaryTree):
            tree_str = ' ' * indent + str(tree.data)
            if not isinstance(tree.left, BinaryTree):
                tree_str += '--> ' + tree.left
            print(tree_str)
            indent = indent + 2
            self.print_parse_tree(tree.left, indent)
            self.print_parse_tree(tree.right, indent)

    def parse(self):
        parse_tree = self._create_tree(self.grammar.start_symbol, [len(self.chart) - 1, 0], 0)
        self.print_parse_tree(parse_tree, 0)

        for i in range(1, self.possible_trees):
            parse_tree = self._create_tree(self.grammar.start_symbol, [len(self.chart) - 1, 0], i)
            self.print_parse_tree(parse_tree, 0)




