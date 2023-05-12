from tree import Node, CreateSyntaxTree, printTree
from InfixPostfix import InfixPostfix
from Automata import *
from Thompson import *
reg = "(↔→↓)|(↔→↓)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9)|(0|1|2|3|4|5|6|7|8|9)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*|(0|1|2|3|4|5|6|7|8|9)+(▪(0|1|2|3|4|5|6|7|8|9)+)?(ε(＋|-)?(0|1|2|3|4|5|6|7|8|9)+)?" 

a = Thompson(reg)
x = 5
y = x
y+=1
print(y)


