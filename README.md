## CNF converter and CYK Parser

Assignment for the Parsing course at the University of Stuttgart

To run the parser **Python 3.5** needs to be installed. All files (main.py, cnf_converter.py, common.py and cyk_parser.py) need to be in the same directory as Python will look to include parts of them as modules.

No additional libraries are required (only the built-in text-processing services `string`, `re` and the functional programming module `itertools` are used).

The parser can be run from the command line as a standalone program:

**The command to run the program is in the following format**:

```
python main.py inputgrammar.txt inputsentences.txt
```

It accepts two arguments: the first one is the path to a text file with the grammar and the second is the path to a text file with the sentences which need to be parsed.

Example calls with the text files which are already included are:

```
python main.py ./grammars/grammar1.txt ./grammars/sentences1.txt
```

and

```
python main.py ./grammars/grammar2.txt ./grammars/sentences2.txt
```

### Input

**Grammar**

In order to return correct results, the input grammar should be in the following form:

S<br/>
S -> NP VP\s\s
NP -> Det Adj N<br/>
NP -> P Det N<br/>
NP -> S<br/>
VP -> V NP<br/>
VP -> N VP<br/>
Det -> 'the'<br/>
Adj -> 'stray' | /<br/>
N -> 'dog' | 'station'<br/>
V -> 'descended'<br/>
P -> 'to'<br/>
V -> 'using'<br/>
N -> 'escalator'<br/>

The start symbol is indicated on the first line. Afterwards each rule starts on a new line. The right and left hand sides are separated by `->`
Every terminal symbol has to be surrounded by quotation marks. To denote an epsilon production, the `/` symbol should be used.

**Sentences**

Example:

the stray dog descended to the station<br/>
the stray dog descended to the station using the escalator<br/>
the using station to stray dog<br/>

Each sentence has to start on a new line and each token has to be separated by spaces from the others.

### Output

The program outputs a message about whether each sentence can be derived from the given grammar as well as parse trees for the sentences which are accepted by the grammar.


### Structure of the program

The program has two main modules: the CNF Converter and the CYK Parser.

In the `common.py` module two classes are defined: `Grammar` and `Rule`. Each instance of the `Grammar` class has as properties a list of rules, terminals, variables and the start symbol. Each instance of the `Rule` class includes as field the left and right hand side of the rule. Some helper functions are included (for example `is_epsilon_production` which are later used for the CNF conversion)

The `CNF converter` follows the steps for the conversion in the following order: Firsty, it removes the appearance of the start symbol on the right hand side, then it eliminates the epsilon productions, afterwards it eliminates unit productions, then replaces terminals which are non-unit productions on the right hand sides and in the end it replaces long productions on the right hand side.

For each step, a WhileLoop is used: it checks whether the grammar currenly contains a rule which does not conform to one of the norms, then it does all necessary replacements; as soon as no more rules that need to be converted are found, the loop is exited.

The `CYK Parser` is a class which is initialized with a grammar and a string (the sentence which needs to be parsed). It includes a function which builds the CYK_Chart at the initialization.
The resulting table includes information about the variables from which every substring can be derived. An instance of the `Backpointer` class is linked to every variable: it stores information about the rule as well as from which cells of the table the variable was derived. This is later used to print the parsing tree.

A class `BinaryTree` is used in order to build recursively the parsing tree. Starting with the node at the top of the table where the start symbol is located, all the next nodes needed for the parse tree are found using the backpointers. At each step the corresponding left and right sides of the tree are added until all terminals are reached.
