from Thompson import Thompson
from Subconjuntos import Closure, get_groups, Subconjuntos2

if __name__=="__main__":
    exp = "(a|c)*c"

    automata = Thompson(exp)
    print(automata.transitions)
    automata.ShowGraph()
    
    afd = Subconjuntos2(automata)
    print(afd.transitions)
    
    print(automata.simulate("acc"))


    
    #automata.ShowGraph()
    #print("transitions: ", afd.transitions)
    #print("start_state: ", afd.start)
    #print("acceptance_states", afd.final)
    #print(afd.simulate("acc"))
    
    #minimized_afd = afd.minimize()
#
    #print("transitions: ", minimized_afd.transitions)
    #print("start_state: ", minimized_afd.start)
    #print("acceptance_states", minimized_afd.final)
    #
    #minimized_afd.ShowGraph()
