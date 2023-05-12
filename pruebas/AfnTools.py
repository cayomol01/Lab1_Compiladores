from Automata import Automata
from Thompson import Thompson
from State import State
from yalex_reader import build_regex


def create_automaton(regexes):
    afns = []
    #for i in regexes:
    #    print(i)
    for i in regexes:
        afn = Thompson(i[1])
        afn.final[0].token = i[0]
        afns.append(afn)
    starter = 1
    inicio = State('s0')

    finals = []
    for i in afns:
        starter = i.changeNames(starter+1)
        finals.append(i.final[0])
        inicio.AddTransition(i.start, 'ε')
    
        
    
        
    
    
    return afns
    
    
def multisimul(afns, cadena):
    for i in afns:
        ans = i.simulate2(cadena)
        if ans[0]== True:
            return ans
    return False

def create(archivo):
    if build_regex(archivo):
        afns = build_regex(archivo)
        return create_automaton(afns)
    else:
        return

if __name__ == "__main__":
    a = create_automaton(build_regex('./yalex/slr-4.yal'))
    print(multisimul(a, '@'))