import State
import matplotlib.pyplot as plt
import networkx as nx
import pydot

#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final


class Automata():
    def __init__(self, start: State, final:State) -> None:
        self.start: State = start
        self.final: State = final
        self.transitions = self.Transiciones()
        self.edges = []
        self.trans_symbols  = {}
        self.alphabet = []
        
    #prints transitions
    def show(self):
        stack = [self.start]
        visited = []
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    print(afn.name, "-->",value,"-->", key.name)
            visited.append(afn)

    
    #pone todas las transiciones en un diccionario
    def Transiciones(self):
        stack = [self.start]
        visited = []
        trans = {}
        while len(stack) != 0:
            afn = stack.pop()
            transiciones = afn.transitions.items()
            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():

                        if value is list:
                            trans[afn.name] = {tuple(value): [key.name, anterior]}
                        else:
                            trans[afn.name] = {value: [key.name, anterior]}
                        
                    #Transiiciones
                    #Trans = transiciones
                    #trans[afn.name] = {nombre del estado actual: {simobolo: estado al que va}}
                    
                    else:
                        if value is list:
    
                            trans[afn.name] = {tuple(value): key.name}
                        else:
                            trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
    
    def getInfo(self):
        self.edges = []
        self.trans_symbols = {}
            
        for i in self.transitions:
            for j in self.transitions[i]:
                if self.transitions[i][j][0]=="s":
                    self.edges.append((i, self.transitions[i][j]))
                    self.trans_symbols[(i,self.transitions[i][j])] = j
                else:
                    for k in self.transitions[i][j]:
                        self.edges.append((i,k))
                        self.trans_symbols[(i,k)] = j
        
    def ShowGraph(self):
        self.getInfo()
        G = nx.DiGraph()
        G.add_edges_from(self.edges)

        pydot_graph = nx.drawing.nx_pydot.to_pydot(G)

        
        
        for edge in G.edges():
            one,two = edge[0], edge[1]
            edge_label = str(self.trans_symbols[(one,two)])
            pydot_edge = pydot.Edge(str(edge[0]), str(edge[1]), label=edge_label)
            pydot_graph.add_edge(pydot_edge)
            
        pydot_graph.get_node(self.start.name)[0].set_style('filled')
        pydot_graph.get_node(self.start.name)[0].set('fillcolor','green')
        
        pydot_graph.get_node(self.final.name)[0].set_style('filled',)
        pydot_graph.get_node(self.final.name)[0].set('fillcolor','red')
        

            
        pydot_graph.write_png('graph.png', encoding="utf-8")

    def getAplhabet(self):
        alphabet = []
        for transitions in self.transitions.values():
            for character in transitions.keys():
                if character not in alphabet and character!="ε":
                    alphabet.append(character)
        return alphabet
            
    
    def subconjuntos(self):
        
        stack = []
        visited = []
        trans = {}
        #
        
        #if simbolo =="epsilon":
            #stack.append(key) (Se añade el estado al que lleva con la transicion epsilon)
            #subconjuntos = [[transiciones epsilon del primer recorrido], [transiciones segundo recorrido]....]
            #subconjuntos[0] = transiciones primer recorrido
            #for subconjuntos[0] (recorrer todos los estados que se encuentran en esa lista)
            #otro for para recorrer los estados de cada uno de los estados en subconjuntos[0]
        while len(stack) != 0:
            #afn -> estado actual en el que se está
            afn = stack.pop()
            
            #Transiciones del estado actual
            transiciones = afn.transitions.items()

            for key, value in transiciones:
                if afn not in visited:
                    stack.append(key)
                    if afn.name in trans.keys():
                        trans[afn.name] = {value: [key.name, anterior]}
                        
                    #Transiiciones
                    #Trans = transiciones
                    #trans[afn.name] = {nombre del estado actual: {simobolo: estado al que va}}
                    
                    else:
                        trans[afn.name] = {value: key.name}
                anterior = key.name
                    
            visited.append(afn)
                
        return trans
    
    def simulate(self, input_str):
        current_states = set(Closure(self.transitions, self.start.name))
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                next_states.update(get_groups(self.transitions, state, symbol))
            current_states = set()
            for state in next_states:
                current_states.update(Closure(self.transitions, state))
        return  self.final.name in current_states
    
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
        closure_states.update(Closure(transiciones, set(state)))
    return closure_states

    
    
