import State
import matplotlib.pyplot as plt
import networkx as nx
from pythomata import SimpleDFA
import pydot
from collections import deque
from queue import Queue



#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final
class AFD():
    def __init__(self, start: str, final:list, transitions: dict) -> None:
        self.start: str = start
        self.final: set = final
        self.transitions = transitions
        self.edges = []
        self.trans_symbols  = {}
        self.alfabeto = self.getAlphabet()
        
    def show(self):
        for key, value in self.transitions.items():
            for symbol, state in value.items():
                print(f"{key} -> {symbol} -> {state}")
                
    
    
    def getInfo(self):
        self.edges = []
        self.trans_symbols = {}
        for i in self.transitions:
            for j in self.transitions[i]:
                if (i, self.transitions[i][j]) in self.trans_symbols.keys():
                    self.trans_symbols[(i,self.transitions[i][j])] += ", " + j
                else:
                    self.edges.append((i, self.transitions[i][j]))
                    self.trans_symbols[(i,self.transitions[i][j])] = " " + j

        
    def ShowGraph(self, name = "graph.png"):
        self.getInfo()
        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        for edge in G.edges():
            one, two = edge[0], edge[1]
            edge_label = str(self.trans_symbols[(one,two)])
            G.edges[(one,two)]['label'] = edge_label
            
        pydot_graph = nx.drawing.nx_pydot.to_pydot(G)


        pydot_graph.get_node(self.start)[0].set_style('filled')
        pydot_graph.get_node(self.start)[0].set('fillcolor', 'green')
        for i in self.final:
            pydot_graph.get_node(i)[0].set_style('filled',)
            pydot_graph.get_node(i)[0].set('fillcolor', 'red')
        
        if self.start in self.final:
            pydot_graph.get_node(self.start)[0].set_style('filled')
            pydot_graph.get_node(self.start)[0].set('fillcolor', 'blue')

        pydot_graph.write_png(name, encoding="utf-8")
        
    def getStates(self):
        states = set(self.transitions.keys())
        for value in self.transitions.values():
            states.update(value.values())
        return states
            

    def getAlphabet(self):
        alphabet = set()
        for transitions in self.transitions.values():
            for character in transitions.keys():
                alphabet.update(character)
        return alphabet
    
    def count_instances(self, matrix):
        count = 0
        for row in matrix:
            for element in row:
                if element == "X":
                    count +=1
        return count

    
    def check_transitions(self, matrix, states):
        est1, est2  = states
        
        #Indices en caso se pueda marcar
        idx1 = int(est1[1:])
        idx2 = int(est2[1:])
        alfabeto = self.getAplhabet()
        
        #Encontrar los estados a los cuales transicionan
        trans1 = self.transitions[est1]
        trans2 = self.transitions[est2]
        
        for i in alfabeto:
            if i in trans1.keys() and i in trans2.keys():
                indice1 = int(trans1[i][1:])
                indice2 = int(trans2[i][1:])
                
                print(f"{est1} ==> {i} ==> {trans1[i]}")
                print(f"{est2} ==> {i} ==> {trans2[i]}\n")
                
                print(matrix[indice1])
                print(matrix[indice1][indice2])
                
                if matrix[indice1][indice2]=="X":
                    matrix[idx1][idx2]="X"
                
        
    def simulate(self, regex):
        state = self.start
        for char in regex:
            if char not in self.transitions[state].keys():
                return False
            state = self.transitions[state][char]
        return state in self.final        
        
    def transition_function(self, state, symbol):
        if symbol in self.transitions[state].keys():
            return self.transitions[state][symbol]
        else:
            return None
                
        
        


    







    ''' def minimize_dfa(self):
        #Utilizar el teorema Myhill-Nerode link: https://www.geeksforgeeks.org/minimization-of-dfa-using-myhill-nerode-theorem/
        #inicializar la tabla con las transiciones
        estados = self.getStates()
        accepting_states = self.final
        non_accepting = estados - self.final
        table = [['' for i in range(len(estados))] for i in range(len(estados))]
        
        for i in range(len(estados)):
            for j in range(i, len(estados)):
                table[i][j] = "O"
                
        if len(non_accepting)==0:
            estado = "S0"
            final = {estado}
            start = estado
            transiciones = {estado:{}}
            for symbol in self.getAplhabet():
                transiciones[estado][symbol]= estado            
            return AFD(start, final, transiciones)
        
        else:
            for i in range(1, len(estados)):
                for j in range(i):
                    qb = "S"+str(j)
                    qa = "S"+str(i)
                    if qa in accepting_states and qb in non_accepting:
                        table[i][j] = "X"
                        
            #Se inicializan los estados que se pueden marcar

            flag = True
            count = self.count_instances(table) #Nos va a servir para llevar el conteo de marcas en la tabla.
            #Si count no cambia significa que se puede cambiar la flag a false y terminar el while loop
            
            #Revisar que otros estados se pueden marcar
            while flag:
                #Recorrer la tabla
                for i in range(1, len(estados)):
                    for j in range(i):
                        #Chequear si (i,j) no esta marcado
                        if table[i][j] == "":
                            qb = "S"+str(j)
                            qa = "S"+str(i)
                            self.check_transitions(table, ("S"+str(i), "S"+str(j)))
                            #Si no esta marcado revisar si con sus transiciones se puede marcar
                            
                if count == self.count_instances(table):
                    flag = False
                else:
                    count = self.count_instances(table)
            #Ahora que ya está llena la tabla, hay que chequear los estados que se pueden combinar
            #Sabemos que se pueden combinar si en la tabla hecha el estado está vacío
            
            new_transitions = {}
            inicial = self.inicial
            new_finals = set()
            for i in range(1, len(estados)):
                    for j in range(i):
                        if table[i][j] == "":
                            
                            nom_estado = f"S{i}S{j}"
                            #Juntar estados
                            estados = set(f"S{i}", f"S{j}")
                            if self.inicial in estados:
                                inicial = nom_estado
                            if estados.intersection(self.final):
                                new_finals.update(nom_estado)
                                
                            
                            
                            pass
                        pass
            
                    
        
        print(self.transitions)
        print(accepting_states)
        print(non_accepting)
        print(table)
        
     '''
     
     
    ''' def minimize(self, max_iterations=1000):
        # Step 1: Create the initial partition
        partition = [self.final, set(self.transitions.keys()) - self.final]

        # Step 2: Initialize the queue
        queue = deque(partition)

        # Step 3: Process the queue
        iterations = 0
        while queue and iterations < max_iterations:
            P = queue.popleft()
            for symbol in self.transitions[self.start]:
                X = {f"S{i}" for i, part in enumerate(partition) if any(next_state in part for state in P
                                                                      for next_state in [self.transitions[state][symbol]])}
                if len(X) < 2:
                    continue
                new_partitions = []
                for part in partition:
                    intersec = part.intersection(X)
                    diff = part.difference(X)
                    if intersec and diff:
                        new_partitions.append(intersec)
                        new_partitions.append(diff)
                    else:
                        new_partitions.append(part)

                partition = new_partitions
                for part in new_partitions:
                    if part not in queue:
                        queue.append(part)

            iterations += 1

        # Step 4: Construct the minimized DFA
        transitions = {}
        for i, part in enumerate(partition):
            for state in part:
                for symbol in self.transitions[state]:
                    next_state = self.transitions[state][symbol]
                    for j, part2 in enumerate(partition):
                        if next_state in part2:
                            transitions.setdefault(f"S{i}", {})[symbol] = f"S{j}"
                            break
        start_state = None
        acceptance_states = set()
        for i, part in enumerate(partition):
            if self.start in part:
                start_state = f"S{i}"
            if part & self.final:
                acceptance_states.add(f"S{i}")
        return AFD(start_state, acceptance_states, transitions)
 '''
