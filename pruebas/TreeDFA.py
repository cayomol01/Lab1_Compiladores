
from tree import Node, CreateSyntaxTree, printTree
from Afd import AFD




def TreeToDFA(regex):
    
    s = regex
    
    root = CreateSyntaxTree(s)
    #root.ShowGraph()
    followpos_table = root.getTable()  
    for i in followpos_table:
        print(i) 
        
    followpos_copy =followpos_table.copy()
        
    new_followpos = []
    ''' while followpos_copy:
        temp = followpos_copy.pop(0)
        new_followpos.append(temp)
        num = temp[1]
        #print(new_followpos)
        for i in range((num), len(followpos_table)):
            if followpos_table[i][2] == temp[2]:
                new_followpos[num-1][2].add(followpos_table[i][1])
                #print('aaa', followpos_table[i])
                #print('bbb', new_followpos)
                #followpos_copy.remove(followpos_table[i]) '''
                
    #print(new_followpos)
    #print(followpos_table)
    
    
    
    
    # Encontramos el alfabeto de la tabla
    alphabet = list(set(entry[0] for entry in followpos_table if entry[0] != "#"))
    #print(alphabet)
    final = followpos_table[-1][1]
    initial =followpos_table[0][1]
    
    trans = [followpos_table[0]]
    stack = [followpos_table[0][2]]
    looked = [followpos_table[0][2]]
    
    stack.append(followpos_table[1][2])
    while stack:
        look_at = stack.pop()
        #print(alphabet)
        for letter in alphabet:
            nodos = set()
            for node in look_at:
                if followpos_table[node-1][0] == letter:
                    nodos.update(followpos_table[node-1][2])
            if nodos not in looked and nodos:
                looked.append(nodos)
                stack.append(nodos)
            trans.append((letter, look_at, nodos))
            
            #print(looked)

    transition = [trans[i] for i in range(len(trans)) if (trans[i][1] and trans[i][2])]

    names = {}
    count = 0
    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if frozenset(a) not in names.keys():
            names[frozenset(a)] = "S"+str(count)
            count+=1
        if frozenset(b) not in names.keys():
            names[frozenset(b)] = "S"+str(count)
            count+=1
         
    transitions = {}  

    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if names[frozenset(a)] not in transitions.keys():
            transitions[names[frozenset(a)]] = {transition[i][0]: names[frozenset(b)]}
        else:
            transitions[names[frozenset(a)]].update({transition[i][0]: names[frozenset(b)]})

    print(transitions)
    start_state = names[frozenset({initial})]
    accepting_states = []
    for key, value in names.items():
        if final in key and value not in accepting_states:
            accepting_states.append(value)
   
    
    # Inicializamos el estado inicial que sería el followpos de nuestro root.
    
    return AFD(start_state, accepting_states, transitions)


def construct_states(regex):
    s = regex
    
    root = CreateSyntaxTree(s)
    #root.ShowGraph()

    followpos_table = root.getTable()  
    for i in followpos_table:
        print(i) 
        

    
    # Encontramos el alfabeto de la tabla
    alphabet = list(set(entry[0] for entry in followpos_table if entry[0] != "#"))
    #print(alphabet)
    final = followpos_table[-1][1]
    initial =followpos_table[0][1]
    
    trans = [followpos_table[0]]
    stack = [followpos_table[0][2]]
    looked = [followpos_table[0][2]]
    
    stack.append(followpos_table[1][2])
    
    #recorrer el 
    
    while stack:
        look_at = stack.pop()
        #print(alphabet)
        for letter in alphabet:
            nodos = set()
            for node in look_at:
                if followpos_table[node-1][0] == letter:
                    nodos.update(followpos_table[node-1][2])
            if nodos not in looked and nodos:
                looked.append(nodos)
                stack.append(nodos)
            trans.append((letter, look_at, nodos))
            
            #print(looked)


    transition = [trans[i] for i in range(len(trans)) if (trans[i][1] and trans[i][2])]

    names = {}
    count = 0
    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if frozenset(a) not in names.keys():
            names[frozenset(a)] = "S"+str(count)
            count+=1
        if frozenset(b) not in names.keys():
            names[frozenset(b)] = "S"+str(count)
            count+=1
         
    transitions = {}  

    for i in range(len(transition)):
        a = transition[i][1]
        b = transition[i][2]
        if type(a) == int:
            a = set({a})
        if type(b) == int:
            b = set({b})
        if names[frozenset(a)] not in transitions.keys():
            transitions[names[frozenset(a)]] = {transition[i][0]: names[frozenset(b)]}
        else:
            transitions[names[frozenset(a)]].update({transition[i][0]: names[frozenset(b)]})

    print(transitions)
    start_state = names[frozenset({initial})]
    accepting_states = []
    for key, value in names.items():
        if final in key and value not in accepting_states:
            accepting_states.append(value)
   
    
    # Inicializamos el estado inicial que sería el followpos de nuestro root.
    
    return AFD(start_state, accepting_states, transitions)



#followpos_table = [('a', 1, {3}), ('b', 2, {3}), ('#', 3, set())]
#dfa = construct_states(followpos_table)
#print(dfa.transitions)

#Revisar estado de inicio, aka: estado 1

#Table = root.getTable
#transitions = {str(Table[0][1]) = }
#stack = [Table[0][2]] == Get Nodes to look at
#stack.append(root)

#while stack:
    #look_at = stack.pop(0)
    
#Seguir la transición con b e ir a todos los nodos que esta en el set
#Ej:
#(b, 1, {2}) -> Goto node 2 -> add node 2 to stack nodes to look at
#node 2 (a, 2, {3,4,5})) -> goto Node {3,4,5} -> add Node {3,4,5} to stack of nodes to look at
#Look at all nodes in {3,4,5} and add all transitions Example: 
#('a', 2, {3, 4, 5})
#('a', 3, {3, 4, 5}) 
#('b', 4, {3, 4, 5})
#('a', 5, {6})
#('b', 6, {7})
#('#', 7, set())

#Union of every transition with an specific character of the alphabet of the regex:
# - Example: alphabet = ["a", "b"]
#Union of transitions of all transitions with a of the nodes to look at, in this case {3,4,5}
#Result {3,4,5,6}
#Union of all transitions with b of the nodes to look at, in this case {3,4,5}
#Result {3,4,5}
#
