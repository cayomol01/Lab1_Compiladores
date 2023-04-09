from tree import Node, CreateSyntaxTree, printTree
from InfixPostfix import InfixPostfix
table = str.maketrans('abc', 'def')
string = 'abcbac'
new_string = string.translate(table)
print(new_string)