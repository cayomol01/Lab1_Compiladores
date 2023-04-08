from Thompson import Thompson
from Subconjuntos import Closure, get_groups, Subconjuntos2
from TreeDFA import TreeToDFA

if __name__=="__main__":
    exp = "ab*ab*"

    automata = Thompson(exp)
    automata.ShowGraph()
    
    afd = Subconjuntos2(automata)
    
    afd2 = TreeToDFA(exp)
    afd2.ShowGraph()
    print(afd2.transitions)
    
    
    


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
