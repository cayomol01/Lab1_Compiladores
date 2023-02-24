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
    if CatchErrors(regex)==False:
        return None
    precedence = {"|": 0, ".": 1, "*": 2, "+": 2, "?": 2}
    newRegex = ""
    
    #Agrega un signo ? cada vez que hay una concatenación
    for i in range(len(regex)):
        if i == len(regex)-1:
            newRegex += regex[i]
        else:
            if regex[i+1] not in precedence.keys() and regex[i+1]!= ")":
                if regex[i] == "*":
                    newRegex += regex[i]
                    newRegex += "."
                elif regex[i] not in precedence.keys() and regex[i]!="(":
                    newRegex += regex[i]
                    newRegex+= "."
                else:
                    newRegex+=regex[i]
            else:
                newRegex +=regex[i]
                
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
        #print("stack: ", operatorStack, "string: ", postfixString)
    while len(operatorStack)!=0:
        postfixString += operatorStack.pop()
    return (postfixString)


def CatchErrors(regex: str):
    operadores = ["|","*","+",".","?"]
    if not regex:
        return False
    
    if regex[0] in operadores:
        return False
    

