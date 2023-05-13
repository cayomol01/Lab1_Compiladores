from Grammar import Grammar

conjuntos = dict()

#Recibe un simbolo y 
def CheckEspsilon(Y, prod):
    if Y in prod.keys():
        return 'ε' in prod[Y]
    return False

def checkLeftRecursiveness(X, productions):
    if X in productions.keys():
        for prod in productions[X]:
            if prod[0]!=X:
                return prod[0]
    else:
        return X
    return False

def primero(grammar: Grammar, X):
    g = grammar
    terminales = g.terminals
    noterminales = g.nonterminals
    producciones = g.prod
    
    if X not in conjuntos.keys():
        conjuntos[X] = []
        
    #Si X es un terminal
    if X in terminales:
        conjuntos[X].append(X)
        return
    temp = list(producciones[X])

    
    #Si se tiene la producción X -> ε
    if 'ε' in producciones[X]:
        conjuntos[X].append('ε')
        temp.remove('ε')
        
    #Recoger solo los temprales que tienen la forma y1y2...
    temp = [i for i in temp if len(i)>=2]
    
    true_temp = [[CheckEspsilon(symbol, producciones) for symbol in prod] for prod in temp]
    
    #Si X es un no terminal y hay una producción de la forma X-> y1y2..yk
    if X in noterminales and temp:
        for prod in range(len(temp)):
            for symbol in range(len(temp[prod])):
                if (new_symbol:=checkLeftRecursiveness(temp[prod][symbol], g.prod)):
                    conjuntos[X].append(primero(g, new_symbol)) #primero(y1) pertenece a primero(X)
                if symbol >0: #Para los siguientes símbolos
                    if all(true_temp[prod][:symbol]):
    
                        new_symbol=checkLeftRecursiveness(temp[prod][symbol], g.prod)
                        conjuntos[X].append(primero(g, new_symbol))
                    elif all(true_temp[prod][symbol]):
                        conjuntos[X].append('ε')
    

    
def siguiente():
    pass


def readYalp(filename):
    tokens = []
    removews = False
    getProductions = False
    productions = {}
    
    trans_table =  {'expression': 'E', 
                    'term': 'T', 
                    'PLUS': '+',
                    'TIMES': '*',
                    'factor': 'F',
                    'LPAREN': '(',
                    'RPAREN': ')',
                    'MINUS': '-',
                    'DIV': '/'}
    
    current_symbol = ""
    
    with open(filename, 'r', encoding='utf-8') as file:
        
        for line in file:
            line = line.strip()
            if line[-1:] == "\n":
                line = line[:-1]
            temp = line.split(" ")
            if temp[0]== "%token":
                tokens.append(temp[1])
            if temp[0]=='IGNORE':
                removews = True
            if temp[0][:2]=="%%":
                getProductions = True
                continue
            if getProductions == True:
                if temp[0]!="" and temp[0]!=";":
                    if len(temp) < 2:
                        idx = line.index(':')
                        symbol = line[:idx]
                        current_symbol = symbol.replace(symbol, trans_table[symbol])
                        productions[current_symbol] = []
                    else:
                        if temp[0]=="|":
                            temp2 = ''.join(temp[1:])
                            for key in trans_table:
                                temp2 = temp2.replace(key, trans_table[key])
                            productions[current_symbol].append(temp2)
                        else:
                            temp2 = ''.join(temp)
                            for key in trans_table:
                                temp2 = temp2.replace(key, trans_table[key])
                            productions[current_symbol].append(temp2)

    return productions, tokens


if __name__ == '__main__':
    prod = readYalp('./Yalp/slr-1.yalp')
    
    p1 = {'E':['E+T|T'], 'T':['T∗F|F']}
    g = Grammar(*prod)
    primero(g, g.initial)
    print(conjuntos)
    print('No Terminales: ', g.nonterminals)
    print('Terminales: ', g.terminals)
    print('Producciones: ', g.prod)
    print('Tokens: ', g.tokens)
    print('Inicial: ', g.initial)