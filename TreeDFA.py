
from tree import Node, CreateSyntaxTree, printTree
from Afd import AFD


def TreeToDFA(regex):
    
    s = regex



    root = CreateSyntaxTree(s)

    followpos_table = root.getTable()    
    
    #Encontramos el alfabeto de la tabla
    alphabet = set([i[0] for i in followpos_table if i!="#"])
    
    transitions = {}  
    states = {} 

    # Inicializamos el estado incicial que sería el followpos de nuestro root.
    start_state = frozenset(followpos_table[0][2])
    # Llevar un conteo de cuales estados ya se revisaron. 
    states[start_state] = False

    # Revisamos cuales de los estados tienen marcados como false
    while any(not processed for processed in states.values()):
        # Encontramos el primer estado no procesado
        current_state = None
        for state, processed in states.items():
            if not processed:
                current_state = state
                break

        # Marcamos como visto
        states[current_state] = True

        # Inicializamos las transiciones para el estado actual
        transitions[current_state] = {}

        # Revisamos las transiciones con cada letra en el alfabeto
        for symbol in alphabet:
            
            # Vemos a que estados se puede llegar con el simbolo
            next_positions = set()
            for position in current_state:
                for followpos_entry in followpos_table:
                    if followpos_entry[1] == position and followpos_entry[0] == symbol:
                        next_positions |= followpos_entry[2]

            # Si después del paso anterior aun hay estados, se añade como nuevo estado
            if next_positions:
                next_state = frozenset(next_positions)
                if next_state not in states:
                    states[next_state] = False
                transitions[current_state][symbol] = next_state

    #Marcamos todos los estados que tienen al estado de aceptación, mejor dicho al estado con valor #
    accepting_states = set()
    for state in states.keys():
        if any(position == len(followpos_table) for position in state):
            accepting_states.add(state)
    
    
    #Cambiar los nombres de los estados de Frozensets a Strings
    count = 0
    contents = {}
    for key in set(transitions.keys()):
        contents[key] = f"S{count}"
        count+=1
        
    for key, value in transitions.items():
        for key2, value2 in value.items():
            transitions[key][key2] = contents[value2]
            
    copy_keys = transitions.copy()
    
    for key in copy_keys.keys():
        transitions[contents[key]] = transitions[key]
        transitions.pop(key)

    start_state = contents[start_state]
    new_accepting = set()
    for i in accepting_states:
        new_accepting.add(contents[i])
        
        
    accepting_states = new_accepting
    return AFD(start_state, accepting_states, transitions)

