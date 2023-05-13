

"""_summary_
    Grammar:
    @prod -> Recibe un diccionario con las diferentes producciones.
    estas producciones ya van sin espacios en blanco y de la
    siguiente manera:
    {'Simbolo': [producciones]}
"""
class Grammar():
    def __init__(self, prod, tokens):
        self.prod =prod
        self.tokens = tokens
        self.nonterminals = []
        self.nonterminals = [i for i in prod.keys() if i not in self.nonterminals]
        self.initial = self.nonterminals[0]
        self.terminals = self.AllTerminals()
        
        
    def AllTerminals(self):
        #Se revisan las producciones
        #self.prod.values = lista de listas [[prod1], [prod2]]
        #Ex: self.prod.values = [['E + T | T']]
        
        #Flatten list prod.values
        allprods = [x for sublist in self.prod.values() for x in sublist]
        terminals = set()
        
        #Get all productions
        for prod in allprods:
            if prod not in self.tokens: 
                for i in range(len(prod)):
                    if prod[i] not in self.nonterminals:
                        if i<len(prod)-2:
                            if prod[i+1]=="'":
                                
                                terminals.update(prod[i]+prod[i+1])
                            else:
                                terminals.update(prod[i])
                        else:
                            terminals.update(prod[i])
            else:
                terminals.add(prod)
        return terminals
    
    #Asocia las producciones a su estado no terminal.
    #Ej: E -> E+T|T  = {'E': ['E+T', T]}
    #Si hay más producciones con E se agregan a esa lista
    def getAllProductions(self, prod):
        for key, value in prod.items():
            #-> ['E+T|T', 'E-T']
            for production in value:
                if '|' in production:
                    temp = production.split('|')
                    self.prod[key].remove(production)
                    self.prod[key].extend(temp)
            
    def AugmentedGrammar(self):
        new_nonterminal = self.initial +"'"
        new_val = [new_nonterminal, *self.nonterminals]
        self.prod[new_nonterminal] = [self.initial]
        self.initial = new_nonterminal
        
        


if __name__ == '__main__':
    prod = {'E':['E+T|T'], 'T':['T∗F|F']}
    
    g = Grammar(prod)
    
    print(g.nonterminals)
    print(g.terminals)
    print(g.prod)