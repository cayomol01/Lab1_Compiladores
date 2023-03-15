from State import State
from Automata import Automata
from InfixPostfix import InfixPostfix


def Thompson(expression:str):
    expression = InfixPostfix(expression)
    print(expression)
    if not expression:
        return None
    stack = []
    # "ε" representa epsilon
    contador = 0
    for i in expression:
        
        #UNION
        #Forma:
        #con epsilon: S0 (inicio) -> s1 
        #con epsilon: S0 (inicio) -> s2
        #con char1: S1 -> S3
        #con char2: S2 -> S4
        #con espsilon: S3 -> S5 (final)
        #con espsilon: S4 -> S5 (final)

        if i == "|":
            inicio = State(name = f's{contador}')
            contador+=1
            end = State(name = f's{contador}')
            afn1 = stack.pop()
            afn2 = stack.pop()
            inicio.AddTransition(afn1.start, "ε") #S0 (inicio) -> S1
            inicio.AddTransition(afn2.start, "ε") #S0 (inicio) -> S2
            afn1.final.AddTransition(end, "ε")    #S3 -> S5 (final)
            afn2.final.AddTransition(end, "ε")    #S4 -> S5 (final)
            afn = Automata(inicio, end)
            stack.append(afn)
            
        
        #CONCATENACIÓN
        #Forma:
        #con char1: S0 (inicio) -> S1
        #con char2: S1 -> S2 (final)
        elif i == ".":
            afn1 = stack.pop()
            afn2 = stack.pop()
            afn2.final.transitions = afn1.start.transitions
            afn = Automata(afn2.start, afn1.final)
            stack.append(afn)
            
        #Estrella de Kleene
        #Forma:
        #con epsilon: S0 (inicio) -> S1 (inicio del automata de stack)
        #con epsilon: S2 (final del automata de stack) -> S1 (inicio del automata de stack)
        #con epsilon: S2 (final del automata de stack) -> S3 (final)
        #con epsilon: S0 (inicio) -> S3 (final)
        
        elif i == "*":
            inicio = State(name = f's{contador}')
            contador+=1
            end = State(name = f's{contador}')
            afn1 = stack.pop()
            inicio.AddTransition(afn1.start, "ε")
            afn1.final.AddTransition(afn1.start, "ε")
            afn1.final.AddTransition(end, "ε")
            inicio.AddTransition(end, "ε")
            afn = Automata(inicio, end)
            stack.append(afn)
            
        #Cerradura de positiva
        #Mismo que cerradura de kleene
        #diferencias:
        #- Hay una transición entre el estado inicial del afn del stack con su estado final y del final al inicial
        #- 
        elif i == "+":
            inicio = State(name = f's{contador}')
            contador+=1
            end = State(name = f's{contador}')
            afn1 = stack.pop()
            inicio.AddTransition(afn1.start, "ε")
            afn1.final.AddTransition(afn1.start, "ε")
            afn1.final.AddTransition(end, "ε")
            afn = Automata(inicio, end)
            stack.append(afn)
            
        elif i == "?":
    
            inicio = State(name = f's{contador}')
            contador+=1
            end = State(name = f's{contador}')
            afn1 = stack.pop()
            inicio.AddTransition(afn1.start, "ε")
            afn1.final.AddTransition(end, "ε")
            inicio.AddTransition(end, "ε")
            afn = Automata(inicio, end)
            stack.append(afn)
            
        #Inicilización de elementos del alfabeto
        #forma:
        #con char: start -> fin
        
        else:
            #print(contador)
            #print(i)
            inicio = State(name = f's{contador}')
            contador+=1
            end = State(name = f's{contador}')
            inicio.AddTransition(end, i)

            

            afn = Automata(start = inicio, final = end)
            stack.append(afn)
        if i!=".":
            contador +=1
    return stack.pop()


   
    
