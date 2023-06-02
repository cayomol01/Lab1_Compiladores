from Grammar import Grammar
from GrammarTools import readYalp, Siguiente, checkTokens
from yalex_reader import build_regex, read_yalex_rules
from AfnTools import createReAfn
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
    def __init__(self,initial_state, grammar):
        self.initial_state = initial_state
        self.conjuntos = [self.initial_state]
        self.grammar = grammar
        self.edges = {}
        self.generateAutomata()
        self.changeNumbers()
        self.changeEdges()
        self.tabla = self.CreateTable()

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
                a = visto[test[1]]
                
            test = multicheck(vis, key[1].newprod)
            
            if test[0]==False:
                visto.append(b)
            else:
                b = visto[test[1]]
                
            new_edges[(a,b)] = value
            
        self.edges = new_edges.copy()
                
            
            
                
            

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
            
    def ShowGraph(self, name="SyntaxAutomata"):
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
            
        
        G.render(filename=name, directory='./outputs',format='png', view=True)
        
    #Retorna todas las transiciones de un número de conjunto dado. 
    def getTransitions(self, number):
        transiciones = {}
        for i in self.edges.keys():
            if i[0].number==number:
                transiciones[self.edges[i]] = i[1].number
        return transiciones
    
    def addEdge(self, number1, number2, transition):
        c = Conjunto(self.initial_state.grammar, number2)
        self.conjuntos.append(c)
        for i in self.conjuntos:
            if i.name == number1:
                c2 = i
        self.edges[(c2, c)] = transition
                
        
    #El parametro cadena será una lista con todos los tokens identificados del archivo
    def Simulation(self, entrada:list):
        grammar = self.grammar
        producciones = {}

        
        count = 1
        for key, value in [(key, value) for key,value in grammar.prod.items() if key!="E'"]:
            for i in value:
                productions = []
                if i !="ID":
                    for j in i:
                        productions.append(j)
                    producciones[count] = {key:productions}
                    count+=1
                else:
                    producciones[count] = {key: [i]}
                    count+=1
        e = entrada
        entrada.append("$")
        pila = [0]
        
        
        while True:
            action = self.tabla["Accion"][e[0]][pila[-1]]
            
            if action[0]=='s':
                pila.append(int(action[1:]))
                e = e[1:]
            elif action[0]=='r':
                #Ej r6
                num = int(action[1:])
                prod = producciones[num]
                key = list(prod.keys())[0]
                for i in range(len(prod[key])):
                    pila.pop()
                pila.append(self.tabla["Ir_a"][key][pila[-1]])
                
            elif action=='ACCEPT':
                return True
            else:
                pila.append(action)
            
            if not entrada:
                return False
                
        

    def CreateTable(self):
        grammar = self.grammar
        
        producciones = {}
        
        count = 1
        for key, value in [(key, value) for key,value in grammar.prod.items() if key!="E'"]:
            for i in value:
                producciones[f'{key}->' + i] = count
                count+=1
        
        non_terminals = grammar.nonterminals
        terminals = grammar.terminals
        
        siguientes = {}
        
        for i in non_terminals: 
            siguientes[i] = list(Siguiente(grammar, i))
        
        terminals.add('$')
        
        tabla = {}
        
        estados = [i for i in range(len(self.conjuntos))]
        
        tabla["Estados"] = estados
        
        tabla["Accion"] = {}
        
        tabla["Ir_a"] = {}
        
        
        for i in terminals:
            tabla["Accion"][i] = ["" for i in range(len(estados))]
            
        tabla["Accion"]['$'][1] = "ACCEPT"
            
        for i in non_terminals:
            tabla["Ir_a"][i] = ["" for i in range(len(estados))]
            
        #Conseguir los shifts para la tabla
        
        for i in tabla["Estados"]:
            trans = self.getTransitions(i)
            for terminal, conjunto in trans.items():
                if terminal in terminals:
                    tabla["Accion"][terminal][i] = f's{conjunto}'
                    
        for i in tabla["Estados"]:
            trans = self.getTransitions(i)
            for nonterminal, conjunto in trans.items():
                if nonterminal in non_terminals:
                    tabla["Ir_a"][nonterminal][i] = conjunto
        

        
        #Conjuntos
        for i in self.conjuntos:
            #Producciones por cada conjunto
            for encabezado, values in i.newprod.items():
                #Revisar si hay un punto al final y no es estado de aceptación
                for prod in values:
                    if prod[-1] == '.' and i.number != 1:
                        #Revisar siguientes para ponerlo en la tabla
                        #{'E': ['a', 'b']...}
                        for key, value in siguientes.items():
                            #Recoger encabezado
                            if key == encabezado:
                                for j in value:
                                    numero = producciones[f'{encabezado}->{prod[:-1]}']
                                    tabla["Accion"][j][i.number] = f'r{numero}'
                                    
        return tabla
    

    
    

                    
                
        
            

        

        
    
            
        
        
        
if __name__ == '__main__':
    
    
    if(prod:=readYalp('./Yalp/slr-1.yalp')):
        afn = read_yalex_rules('./Yalp/slr-1.yal')
        if(checkTokens(afn[1].values(), prod[1])):
            g = Grammar(*prod)
            
            prod = readYalp('./Yalp/slr-1.yalp')
            prod2 = readYalp('./Yalp/slr-1.yalp')

            print(" ")
            print('No Terminales: ', g.nonterminals)
            print('Terminales: ', g.terminals)
            print('Producciones: ', g.prod)
            print('Tokens: ', g.tokens)
            print('Inicial: ', g.initial)
            print(" ")
            

            
            #p = {}
            #s = {}
            #for i in g.nonterminals:
            #    p[i] = First2(g,i)
            #    s[i] = list(Siguiente(g, i))
            #print(f'Primero: {p}')
            #print(f'Siguiente: {s}')
            
            prod = readYalp('./Yalp/slr-1.yalp')
            prod2 = readYalp('./Yalp/slr-1.yalp')

            
            g = Grammar(*prod)
            g.AugmentedGrammar()
            
            g1 = Grammar(*prod2)
            g1.AugmentedGrammar()
            
            print(g.prod)
            
            #print(g.tokens)

            c0 = Conjunto(g, 0, corazon={g.initial: g.prod[g.initial]})
            a1 = SyntaxAutomata(c0, g1)

            
            
            l = ['ID', '*', 'ID', '+', 'ID']
            print(a1.Simulation(l))
                    
            
            #s = siguiente(g, p, X=g.initial)
            #print(f'Siguiente {s}')
            #
            #g.AugmentedGrammar()
            #
            #c0 = Conjunto(g, 0, corazon={g.initial: g.prod[g.initial]})
#
            #a1 = SyntaxAutomata(c0)
            #
            #a1.ShowGraph()
        else:
            print('Los tokens no son iguales entre archivos')