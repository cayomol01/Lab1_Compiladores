from Grammar import Grammar
from yalex_reader import build_regex, read_yalex_rules
from AfnTools import createReAfn

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


def First2(grammar, X):
    g = grammar
    terminals = g.terminals
    nonterminals = g.nonterminals
    productions = g.prod
    
    
    if X in terminals:
        return X
    else:
        conjunto = []
        if 'ε' in productions[X]:
            conjunto.append('ε')
            
        for prod in productions[X]:
            if prod in terminals:
                conjunto.append(First2(g, prod))
            else:
                if prod[0]!=X:
                    if len(prod)>1:
                        if prod[0] in terminals:
                            conjunto.append(First2(g, prod[0]))
                            continue
                        else:
                            count = 0
                            for i in range(len(prod)-1):
                                conjunto.append(First2(g, prod[i]))
                                if 'ε' in productions[prod[i]] and count == i:
                                    conjunto.append(First2(g, prod[i+1]))
                                    count+=1
                            count = 0
                            for i in range(len(prod)):
                                if 'ε' in productions[prod[i]] and count == i:
                                    conjunto.append(First2(g, prod[i+1]))
                                    count+=1
                            conjunto.append(First2(g, 'ε'))
                                
                    else:
                        conjunto = [*First2(g, prod)]
    return conjunto
    
    ''' if primeros is None:
        primeros = {}
        for nt in grammar.nonterminals:
            primeros[nt] = set()

    if X in grammar.terminals:
        primeros[X].add(X)
    else:
        for prod in grammar.prod[X]:
            if len(prod) > 0:
                first_simbolo = prod[0]

                # If it's a nonterminal, recursively compute its First set
                if first_simbolo in grammar.nonterminals:
                    First(grammar, first_simbolo, primeros)

                    # Update First(X) with First(Y1) - {ε}
                    primeros[X].update(primeros[first_simbolo] - {'ε'})

                    # If First(Y1) contains ε, continue with the next symbol in the production
                    if 'ε' in primeros[first_simbolo]:
                        i = 1
                        while i < len(prod) and 'ε' in primeros[first_simbolo]:
                            next_simbolo = prod[i]
                            if next_simbolo in grammar.terminals:
                                primeros[X].add(next_simbolo)
                                break
                            else:
                                First(grammar, next_simbolo, primeros)
                                primeros[X].update(primeros[next_simbolo] - {'ε'})
                                if 'ε' not in primeros[next_simbolo]:
                                    break
                            i += 1

                # If it's a terminal, add it to First(X)
                elif first_simbolo in grammar.terminals:
                    primeros[X].add(first_simbolo)

            # If the production is empty, add ε to First(X)
            else:
                primeros[X].add('ε')

    return primeros '''


def Siguiente(grammar: Grammar, X):
    g = grammar
    terminals = g.terminals
    nonterminals = g.nonterminals
    productions = g.prod
    
    conjunto = []
    new_prod = []
    
    if X == g.initial:
        conjunto.append('$')
        
    for key, value in productions.items():
        for i in value:
            if X in i and i not in terminals:
                new_prod.append((key,i))
  
  
    for key, value in new_prod:
        idx = value.index(X)
        if idx != len(value)-1:
            datos = [i for i in First2(g, value[idx+1]) if i!="ε"]
            conjunto.extend(datos)
        if (idx!=len(value)-1 and 'ε' in First2(g, value[2])) or (value[-1]==X):
            if key !=X:
                conjunto.extend(Siguiente(g, key))
                
    return set(conjunto)

    
    
        

    


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