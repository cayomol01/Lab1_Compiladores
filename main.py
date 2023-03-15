from Thompson import Thompson
from Subconjuntos import Subconjuntos, Closure, get_groups, Subconjuntos2

if __name__=="__main__":
    exp = "(a|b)*"

    automata = Thompson(exp)
    #automata.ShowGraph()
    #print(Closure(automata.transitions, 's5'))
    print(get_groups(automata.transitions, ['s5', 's7', 's4', 's0', 's2', 's3'], 'a'))
    print(Subconjuntos2(automata))
