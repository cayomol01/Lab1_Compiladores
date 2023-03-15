from Automata import Automata

def Closure(transiciones: dict, state: str):
    epsilon = "ε"
    visited = {state}
    stack = [state]
    
    while stack:
        estado = stack.pop()
        if estado in transiciones and epsilon in transiciones[estado]:
            epsilon_transitions = transiciones[estado][epsilon]
            if isinstance(epsilon_transitions, list):
                for t in epsilon_transitions:
                    if t not in visited:
                        stack.append(t)
                        visited.add(t)
            else:
                if epsilon_transitions not in visited:
                    stack.append(epsilon_transitions)
                    visited.add(epsilon_transitions)
    return visited
        
def list_eq(list1: list, list2: list):
    return set(list1)==set(list2)

#Para esta función se ingresa lista de estados (de la clausura epsilon) y las transiciones del AFND
def get_groups(transiciones: dict, estados:list, character: str):
    group = set()
    for i in estados:
        if i in transiciones and character in transiciones[i]:
            if isinstance(transiciones[i][character], list):
                group.update(transiciones[i][character])
            else:
                group.add(transiciones[i][character])
                
    closure_states = set()
    for state in group:
        closure_states.update(Closure(transiciones, state))
    return closure_states
                
            
        
        
        
    
        

def Subconjuntos(AFN: Automata):
    transiciones = AFN.transitions
    alphabet = AFN.getAplhabet()
    #State name
    count = 0
    state = "S"+str(count)
    
    #stack
    
    #inicializar los grupos 
    groups = {state: Closure(transiciones, AFN.start.name)}
    stack = [state]
    transitions = {}
    
    while stack:
        transitions.update({state:{}})
        estado = stack.pop()
        for i in alphabet:
            grupos_copy = groups.copy()
            #transitions['s0']['a']
            #{'s0': {'a': [grupo_cerradura a]}}
            grupos = get_groups(transiciones, groups[estado], i)
            
            #grupos = ['s0', 's1']
            
            #Encontrar los grupos con la letra del alfabeto
            #es decir que un los el e closure con la letra a.
            
            #chequear si ese grupo ya está en los grupos que ya tengo
            #junto con su estado. Es decir que su estado ya fue creado
            
            #Si el estado ya fue creado entonces solo agregar los grupos
            #encontrados junto a su símbolo de transición en transitions
            
            #Si el estado no ha sido creado. Aumentar 1 al counter y 
            #concatenar el numero con S.
            #- Luego agregar el estado nuevo al stack por revisar.
            #- Agregar el estado junto con su grupo a groups
            #- Agregar a transiciones el simbolo con su nuevo estado creado
            
            
            if grupos: 
                for seen_state, seen_group in  grupos_copy.items():

                    #Si el grupo ya existe dentro de los grupos creados
                    if list_eq(grupos, seen_group):
                        transitions[estado][i] = seen_state
                    #si no existe dentro de los grupos creados
                    #Agregar a los grupos
                    else:
                        #Aumentar el numero de estado
                        count+=1
                        state = "S"+str(count)
                        
                        #Agregar al stack para revisar sus transiciones
                        stack.append(state)
                        
                        #Agregar a grupos
                        groups[state] = grupos
                        
                        #Agregar la transición a el diccionario de transiciones
                        transitions[estado][i] = state
                    
def Subconjuntos2(AFN: Automata):
    transiciones = AFN.transitions
    alphabet = AFN.getAplhabet()
    #State name
    count = 0
    state = "S"+str(count)
    
    #stack
    
    #inicializar los grupos 
    groups = {state: Closure(transiciones, AFN.start.name)}
    stack = {state}
    transitions = {}
    
    while stack:
        estado = stack.pop()
        transitions[estado] = {}
        new_groups = {}
        for i in alphabet:
            grupos = set()
            for state in groups[estado]:
                grupos |= set(get_groups(transiciones, [state], i))
            if grupos: 
                seen_state = None
                for s, g in groups.items():
                    if grupos == g:
                        seen_state = s
                        break
                if seen_state:
                    transitions[estado][i] = seen_state
                else:
                    count += 1
                    state = "S" + str(count)
                    stack.add(state)
                    new_groups[state] = grupos
                    transitions[estado][i] = state
        groups.update(new_groups)
    return transitions  
        
    print(AFN.getAplhabet())
    print(Closure(transiciones, AFN.start.name))
    print(transitions)
    

    