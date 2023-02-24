import State
import matplotlib.pyplot as plt
import networkx as nx

#Clase Automata para el algoritmo de thompson

#Automata tiene un estado inicial y uno final, estado de aceptación
#start - Estado inicial
#final - Estado final
class Automata():
    def __init__(self, start: State, final:State) -> None:
        self.start = start
        self.final = final
        self.transitions = self.Transiciones()
        self.edges = []
        self.trans_symbols  = {}
        
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
                        trans[afn.name] = {value: [key.name, anterior]}
                        
                    #Transiiciones
                    #Trans = transiciones
                    #trans[afn.name] = {nombre del estado actual: {simobolo: estado al que va}}
                    
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
                for k in self.transitions[i][j]:
                    self.edges.append((i,k))
                    self.trans_symbols[(i,k)] = j
    
    def ShowGraph(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        pos = nx.spring_layout(G)
        plt.figure()
        colores = []

        for nodo in G.nodes:
                # print(nodo)
                colores.append('lightgreen' if nodo == 'q0' else  "pink" if nodo== self.final else   'lightblue')
                

        nx.draw(
            G, pos, edge_color='black', width=1, linewidths=1, node_color=colores,
            node_size=500, alpha=0.9,
            labels={node: node for node in G.nodes()}
        )
        # nx.draw_networkx(G, node_color=colores, with_labels=True)

        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=self.trans_symbols,
            font_color='red'
        )

        plt.show()
    
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
            
    
    
    
