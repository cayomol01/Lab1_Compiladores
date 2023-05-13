from Grammar import Grammar
from yalex_reader import build_regex, read_yalex_rules
from AfnTools import createReAfn
from ConjuntoAutomata import Conjunto, SyntaxAutomata

conjuntos = dict()

#res1 = {'E': ['(', 'ID'], 'T': ['(', 'ID'], 'F': ['(', 'ID']}
#res2 = {'E': ['$', '+', ')'], 'T': ['*','$', '+', ')'], 'F': ['*','$', '+', ')']}

res1 = {}
res2 = {}

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
    if not grammar:
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
    return res1
        

    
def siguiente(grammar, res_primero, X = None):
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
    if not grammar:
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
    return res2


def remove_comments(line):
    if "/*" in line:
        line = line[:line.index("/*")] + line[line.index("*/") + 2:]
    return line


def checkComments(line):
    if "/*" in line:
        return( "*/" in line[line.index("/*"):])
    if "*/" in line:
        return( "/*" in line[:line.index("*/")])
    else:
        return True
    
def checkTokenStructure(line):
    if line[0]!="%":
        return False
    if len(line.split(' '))>2:
        return False
    if line.count('%')>1 and len(line)>2:
        return False
    if line[1]==" ":
        return False
    return True

def checkProductionStructure(line):
    
    if line[0]!="|":
        return False
    if line.count('|')>1:

        return False
    if line[1]!=" ":
        return False
    return True
    
    

def readYalp(filename):
    tokens = []
    errors = []
    line_counter = 1

    
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
            
            # Remove comments and strip
            if checkComments(line)==False:
                errmess = f"Error en la línea {line_counter}. Comentario mal definido"
                errors.append(errmess)

            else:
                line = remove_comments(line.strip())
                
          
            
            if line[-1:] == "\n":
                line = line[:-1]
            temp = line.split(" ")
            if "%" in temp[0] and getProductions == False and '%%' not in temp[0]:
                if checkTokenStructure(line)==False:
                    errmess = f"Error en la línea {line_counter}. Token mal definido"
                    errors.append(errmess)
                else:
                    tokens.append(temp[1])
            if temp[0]=='IGNORE':
                removews = True
            if temp[0][:2]=="%%":
                getProductions = True
                line_counter+=1

                continue
            if getProductions == True:
                if temp[0]!="" and temp[0]!=";":
                    if len(temp) < 2 and ':' in temp[0]:
                        idx = line.index(':')
                        symbol = line[:idx]
                        current_symbol = symbol.replace(symbol, trans_table[symbol])
                        productions[current_symbol] = []
                    else:
                        if len(productions[current_symbol])>0:
                            if checkProductionStructure(line)==False:
                                errmess = f"Error en la línea {line_counter}. Error en la estructura de la produccion definida"
                                errors.append(errmess)
                            else:
                                temp2 = ''.join(temp[1:])
                                for key in trans_table:
                                    temp2 = temp2.replace(key, trans_table[key])
                                productions[current_symbol].append(temp2)
                        else:
                            temp2 = ''.join(temp)
                            for key in trans_table:
                                temp2 = temp2.replace(key, trans_table[key])
                            productions[current_symbol].append(temp2)
            line_counter+=1
    if errors:
        for i in errors:
            print(i)
        return None

    return productions, tokens



def checkTokens(l1, l2):

    for token in l2:
        if token not in l1:
            return False
    return True


if __name__ == '__main__':
    if(prod:=readYalp('./Yalp/slr-1.yalp')):
        afn = read_yalex_rules('./Yalp/slr-1.yal')
        if(checkTokens(afn[1].values(), prod[1])):
            g = Grammar(*prod)
            print(" ")
            print('No Terminales: ', g.nonterminals)
            print('Terminales: ', g.terminals)
            print('Producciones: ', g.prod)
            print('Tokens: ', g.tokens)
            print('Inicial: ', g.initial)
            print(" ")
            
            p = primero(g, g.initial)
            print(f'Primero: {p}')
            
            s = siguiente(g, p, X=g.initial)
            print(f'Siguiente {s}')
            
            g.AugmentedGrammar()
            
            c0 = Conjunto(g, 0, corazon={g.initial: g.prod[g.initial]})

            a1 = SyntaxAutomata(c0)
            
            a1.ShowGraph()
        else:
            print('Los tokens no son iguales entre archivos')