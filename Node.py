class Node:
    def __init__(self, symbol, backpointers):
        self.symbol = symbol
        self.backpointers = backpointers


class Backpointer:
    def __init__(self, rule, cell1, cell2):
        self.rule = rule
        self.cell1 = cell1
        self.cell2 = cell2