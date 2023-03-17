from tree import Node, CreateSyntaxTree, printTree
from InfixPostfix import InfixPostfix

s = "(a|)*abb"


a = {1, 2, 3}
b = ('b', 2, {1, 2, 3})

print(1 in a)
print(1 in b[2])
root = CreateSyntaxTree(s)

nodos = root.getTable()
for i in nodos:
    print(i)
