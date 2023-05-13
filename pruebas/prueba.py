from tree import Node, CreateSyntaxTree, printTree
from InfixPostfix import InfixPostfix
from Automata import *
from Thompson import *
reg = "(↔→↓)|(↔→↓)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9)|(0|1|2|3|4|5|6|7|8|9)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*|(0|1|2|3|4|5|6|7|8|9)+(▪(0|1|2|3|4|5|6|7|8|9)+)?(ε(＋|-)?(0|1|2|3|4|5|6|7|8|9)+)?" 

a = Thompson(reg)
x = 5
y = x
y+=1

tokens = ['id']

def moveDot(prod):
        print(prod)
        if prod.replace('.','')in tokens:
            idx = prod.index('.')+len(prod)
            prod = prod.replace('.', '')
            new_prod = prod[:idx] + '.' + prod[idx:]
        else: 
            idx = prod.index('.')
            prod = prod.replace('.', '')
            new_prod = prod[:idx+1] + '.' + prod[idx+1:]
        return new_prod 

# .E
# 0 1
# E
# 0
#
prov = '.id'
a = [{'a': ['a', 'b'], 'b': ['c', 'd']}, {'c': ['a', 'b'], 'b': ['c', 'd']}]
b = {'a': ['b', 'a'], 'b': ['d', 'c']}



#checks if two dictonaries have the same elements
def checkEquality(a,b):
    print(a)
    if a.keys()!=b.keys():
        return False
    #Tienen las mismas keys por lo tanto podemos recorrer solo uno de los diccionarios
    for key, value in a.items():
        c = set(a[key])
        d = set(b[key])
        if c !=d:
            return False
        
    return True


def multicheck(a_list, b):
    b_list = []
    for a in a_list:
        b_list.append(checkEquality(a,b))
    for i in b_list:
        if i == True:
            return True
    return False

c =  multicheck(a,b)


g = 'aaaaa'
d = 'bbbbb'

h = [g,d]

print('\n'.join(h))



b = [True, True, True, False]

c = ['a', 'b']
c[0] = '.'+c[0]
print(c)
print(b[:-1], all(b[:-1]))
