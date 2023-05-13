from Grammar import Grammar
from GrammarTools import readYalp
import networkx as nx
import pydot
from graphviz import Digraph


#checks if two dictonaries have the same elements
def checkEquality(a,b):
    if a.keys()!=b.keys():
        return False
    #Tienen las mismas keys por lo tanto podemos recorrer solo uno de los diccionarios
    for key, value in a.items():
        c = set(a[key])
        d = set(b[key])
        if c !=d:
            return False

    return True


def multicheck(a_list, b):
    b_list = []
    for a in a_list:
        b_list.append(checkEquality(a,b))
    for i in range(len(b_list)):
        if b_list[i] == True:
            return True, i
    return False, -1

class Conjunto():
    def __init__(self, grammar: Grammar, numero, corazon= None):
        self.number = numero
        self.grammar = grammar  
        self.allprod = self.grammar.prod
        self.corazon = corazon or {}
        self.initial = list(self.corazon.keys())[0]
        self.addDot()
        self.resto = self.Cerradura()
        self.newprod = self.newProducciones()

        
    def addDot(self):
        
        for key, value in self.allprod.items():
            for i in range(len(value)):
                if self.allprod[key][i][0]!='.':
                    self.allprod[key][i] = '.'+value[i]
                #print(self.allprod[key], self.allprod[key][i])

    #Se necesita un corazon
    def Cerradura(self):
        corazon = self.corazon
        production = self.corazon[self.initial][0]
        dot_idx = production.index('.')
        cerradura = {}

        if dot_idx < len(production)-1:
            ini_lookat = production[dot_idx+1]
            if ini_lookat not in self.grammar.terminals:
                stack = [ini_lookat]
                vistos = [ini_lookat]
                
                
                while stack:
                    
                    lookat = stack.pop()
                    
                    if lookat not in cerradura.keys():
                        cerradura[lookat] = []
                    
                    if lookat in self.grammar.nonterminals:
                        cerradura[lookat].extend(self.allprod[lookat])
                        for i in self.allprod[lookat]:
                            idx = i.index('.')
                            if idx < len(i)-1 and i[idx+1] in self.grammar.nonterminals and i[idx+1] not in vistos:
                                stack.append(i[idx+1])
                                vistos.append(i[idx+1])
                                    
        return cerradura
    
    def moveDot(self, prod):
        if prod.replace('.', '') in self.grammar.tokens:
            idx = prod.index('.')+len(prod)
            prod = prod.replace('.', '')
            new_prod = prod[:idx] + '.' + prod[idx:]
        else:
            idx = prod.index('.')
            prod = prod.replace('.', '')
            new_prod = prod[:idx+1] + '.' + prod[idx+1:]
        return new_prod 
    
    def newProducciones(self):
        new_dict = {}
        for key, value in self.corazon.items():
            if key in new_dict.keys():
                new_dict[key].extend(value)
            else:
                new_dict[key] = []
                new_dict[key].extend(value)
        
        for key, value in self.resto.items():
            if key in new_dict.keys():
                new_dict[key].extend(value)
            else:
                new_dict[key] = []
                new_dict[key].extend(value)
           
        return new_dict
                    
    def Ir_A(self, X):
        producciones = self.newprod
        
        new_corazon = {}
        #Tengo que revisar las producciones que tienen esto .
        for key, value in producciones.items():
            for prod in value:
                if f'.{X}' in prod:
                    new_corazon[key] = prod
        for key,prod in new_corazon.items():
            new_corazon[key] = [self.moveDot(prod)]
            
        return Conjunto(self.grammar, self.number+1, corazon=new_corazon.copy())
        #Recorrer todas las producciones que dan .X:
        #Si la producción contiene .X
        #entonces:
            #new_corazon[key] = value
        #for key, prod in new_corazon:
        #   new_corazon[key] = moveDot(prod)
        #return Conjunto(self.g, self.numero+1, corazon=new_corazon.copy())



class SyntaxAutomata():
    def __init__(self,initial_state):
        self.initial_state = initial_state
        self.conjuntos = [self.initial_state]
        self.edges = {}
        self.generateAutomata()
        self.changeNumbers()
        #self.changeEdges()

    def changeNumbers(self):
        for i in range(len(self.conjuntos)):
            self.conjuntos[i].number = i
            
    def changeEdges(self):
        edges = self.edges
        new_edges = {}
        
        visto = []
        
        #key -> tuple (conjunto1, conjunto2)
        #value -> transition_symbol
        for key, value in self.edges.items():
            a = key[0]
            b = key[1]
            vis = [i.newprod for i in visto]
            test =  multicheck(vis, key[0].newprod)
            
            if test[0]==False:
                visto.append(a)
            else:
                a = test[1]
                
            test = multicheck(vis, key[1].newprod)
            
            if test[0]==False:
                visto.append(b)
            else:
                b = test[1]
                
            new_edges[(a,b)] = value
                
            
            
                
            
        pass

    #Esta función sirve para sacar todos los conjuntos que pueden salir de un conjunto dado
    #Usa la función Ir_a para sacar dichos conjuntos. 
    def getConjuntos(self, conjunto:Conjunto):
        c = conjunto
        g = c.grammar
        prod = conjunto.newprod
        vistos = []
        
        conjuntos = []
        
        for value in prod.values():
            for prod in value:
                if prod.replace('.', '') in g.tokens:
                    
                    idx = prod.index('.')
                    if idx!=len(prod)-1:
                        if prod[idx+1:] not in vistos:
                            vistos.append(prod[idx+1:])
                            c2 = c.Ir_A(prod[idx+1:])
                            conjuntos.append(c2)
                            self.edges[(c, c2)]= prod[idx+1:]
                else:
                    idx = prod.index('.')
                    if idx!=len(prod)-1:
                        if prod[idx+1] not in vistos:
                            vistos.append(prod[idx+1])
                            c2 = c.Ir_A(prod[idx+1])
                            #print(prod[idx+1], c2.newprod)
                            conjuntos.append(c2)
                            self.edges[(c, c2)]= prod[idx+1]

        return conjuntos
    
    #Función para generar el automata completo
    def generateAutomata(self):
        
        visitado = []
        stack = [self.initial_state]
        
        while stack:
            lookat = stack.pop()
            conjuntos = self.getConjuntos(lookat)
            for i in conjuntos:
                vis = [i.newprod for i in visitado]
                if multicheck(vis, i.newprod)[0]==False:
                    visitado.append(i)
                    stack.append(i)
                    self.conjuntos.append(i)
            
    def showEdges(self):
        count = 1
        for key, value in self.edges.items():
            print(f'Conjunto = {count}')
            print(f'1. {key[0].newprod}')
            print(f'2. {key[1].newprod}')
            print(f'-> {value}')
            print('')
            count +=1
            
    def ShowGraph(self, name="graph.png"):
        G = Digraph(encoding='utf-8')
        
        for i in self.conjuntos:
            x = []
            for key, value in i.newprod.items():
                for prod in value:
                    x.append(f'{key} → {prod}')
            
            a = f'I{i.number}\n'
            a += '\n'.join(x)
            G.node(str(i.number), a)
        
        for key, value in self.edges.items():
            G.edge(str(key[0].number), str(key[1].number), label=value)
            
        
        G.render(filename='SyntaxAutomata', directory='./outputs',format='png', view=True)

        
    
            
        
        
        
if __name__ == '__main__':
    if __name__ == '__main__':
        prod = readYalp('./Yalp/slr-1.yalp')
    
    p1 = {'E':['E+T|T'], 'T':['T∗F|F']}
    g = Grammar(*prod)
    g.AugmentedGrammar()
    #print(g.tokens)

    c0 = Conjunto(g, 0, corazon={g.initial: g.prod[g.initial]})
    
    a1 = SyntaxAutomata(c0)
    

    a1.ShowGraph()
    #for i in b:
    #    print(i.newprod)
    count = 1
   
    #b = a1.getConjuntos(c0)
    

    #print(c0.corazon)
    #print('aaaaaa', c0.resto)
    #c1 = c0.Ir_A('E')
    #print(c1.newprod)
    #print(c1.corazon)
    #print(" ")
    #
    #c2 = c1.Ir_A('+')
    #print(c2.corazon)
    #print(c2.resto)
    #print(" ")
    #
    #c3 = c2.Ir_A('T')
    #print(c3.corazon)
    #print(c3.resto)
    #print(" ")
    #
    #c4 = c3.Ir_A('*')
    #print(c4.corazon)
    #print(c4.resto)
#
    ##print('No Terminales: ', g.nonterminals)
    ##print('Terminales: ', g.terminals)
    #print('Producciones: ', g.prod)
    #print('Tokens: ', g.tokens)
    #print('Inicial: ', g.initial)