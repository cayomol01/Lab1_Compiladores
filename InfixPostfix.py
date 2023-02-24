import re


#Convertir la expresión de infix (normal) a postfix
#params:
#@regex -> str Expresión regular a convertir
def InfixPostfix(regex:str):
    #precedence = {"+": 0, "-": 0, "*": 1, "/":1, "^":2, }
    #Símbolos son: 
    # | -> or
    # * -> cerradura de kleene
    # + -> cerradura positiva
    # . -> concatenación
    # ? -> Cero o una vez
    #{}
    precedence = {"+": 0, "?": 1, "*": 2}
    newRegex = ""
    
    #Agrega un signo ? cada vez que hay una concatenación
    for i in range(len(regex)):
        if i == len(regex)-1:
            newRegex += regex[i]
        else:
            if regex[i+1] not in precedence.keys() and regex[i+1]!= ")":
                if regex[i] == "*":
                    newRegex += regex[i]
                    newRegex += "?"
                elif regex[i] not in precedence.keys() and regex[i]!="(":
                    newRegex += regex[i]
                    newRegex+= "?"
                else:
                    newRegex+=regex[i]
            else:
                newRegex +=regex[i]
                
    print(newRegex)
    postfixString = ""
    operatorStack = []
    regex = newRegex
    #convertir infix postfix
    for i in regex:
        #print(i)
        if i in precedence.keys() or i=="(" or i == ")":
            if len(operatorStack)==0 or operatorStack[-1]=="(" or i == "(":
                operatorStack.append(i)
            elif i == ")":
                check = ""
                while check!="(":

                    postfixString += operatorStack.pop()
                    check = operatorStack[-1]
                operatorStack.pop()
            elif precedence[i] < precedence[operatorStack[-1]]:
                while precedence[i] < precedence[operatorStack[-1]]:
                    postfixString += operatorStack.pop()
                    if len(operatorStack) == 0 or operatorStack[-1]=="(":
                       break
                operatorStack.append(i)
            elif precedence[i] > precedence[operatorStack[-1]]:
                operatorStack.append(i)
            elif precedence[i] == precedence[operatorStack[-1]]:
                postfixString += operatorStack.pop()
                operatorStack.append(i)
                
        else:
            postfixString += i
        print(i, operatorStack, postfixString)
        #print("stack: ", operatorStack, "string: ", postfixString)
    while len(operatorStack)!=0:
        postfixString += operatorStack.pop()
    print(f"{regex} -> {postfixString}")
    return (postfixString)


def CatchErrors(regex: str):
    operadores = ["|","*","+",".","?"]
    
    
    # Verificando que la expresión tenga paréntesis de apertura y cierre.

    # Verificando que la expresión tenga letras o números.
    coin = re.match(r"[a-zA-Z0-9ε]+", regex)

    if not coin:
        print("Error: La expresión regular no tiene letras o números.")
        #print("Error: La expresión regular no puede tener números y letras.")
        return False


    # Verificando que la expresión no tenga un * o un + al inicio.
    coincidencia = re.match(r"^(?![*+]).*", regex)

    if not coincidencia:
        print("Error: La expresión regular no puede empezar con un * o un +.")
        return False