import re

PRECEDENCE = { "|": 0, ".": 1, "*": 2, "+": 2, "?": 2}



def convert_positive_kleene(regex):
    new_regex = ""
    adder = 0
    for i  in range(len(regex)):
        if regex[i]=="+":
            if regex[i-1]==")":
                count = i-1+adder                
                temp_string = ""
                while new_regex[count]!="(":
                    temp_string+=new_regex[count]
                    count-=1
                temp_string+="("
                temp_string = temp_string[::-1]+"*"
                adder+=len(temp_string)-1
                new_regex+=temp_string
            else:
                new_regex+=regex[i-1]+"*"
                adder+=1
        elif regex[i]=="?":
            if regex[i-1]==")":
                count = i-1+adder
                temp_string = ""
                while new_regex[count]!="(":
                    temp_string+=new_regex[count]
                    count-=1
                    
                temp_string+="(("
                temp_string = temp_string[::-1]+"|ε)"
                adder+=3
                remover = len(temp_string)-4
                new_regex= new_regex[:len(new_regex)-remover] + temp_string
                
                
            else:
                new_regex+=regex[i-1]+"*"
                adder+=1
            
        else:
            new_regex+=regex[i]
    return new_regex
                    
 
                    
     
def shunting_yard(regex):
    output = []
    opstack = []
    precedence = {'|': 0, '.': 1, '*': 2, '+': 2, '?': 2}
    
    for c in regex:
        if c not in precedence.keys() and c !="(" and c!=")":
            output.append(c)
        elif c == '(':
            opstack.append(c)
        elif c == ')':
            while opstack and opstack[-1] != '(':
                output.append(opstack.pop())
            if opstack and opstack[-1] == '(':
                opstack.pop()
        else:
            while opstack and precedence[c] <= precedence.get(opstack[-1], -1):
                output.append(opstack.pop())
            opstack.append(c)
    
    while opstack:
        output.append(opstack.pop())
    
    return ''.join(output)


def InfixPostfix(regex:str):
    #precedence = {"+": 0, "-": 0, "*": 1, "/":1, "^":2, }
    #Símbolos son: 
    # | -> or
    # * -> cerradura de kleene
    # + -> cerradura positiva
    # . -> concatenación
    # ? -> Cero o una vez
    #{}
    
    regex = convert_positive_kleene(regex)
    if CatchErrors(regex)==False:
        return 
    precedence = {"|": 0, ".": 1, "*": 2, "+": 2, "?": 2}
    newRegex = ""
    
    #Agrega un signo . cada vez que hay una concatenación
    
    #(↔ → ↓)|(↔→↓)+|(A|B|C|D)
    for i in range(len(regex)):
        if i == len(regex)-1:
            newRegex += regex[i]
        else:
            if regex[i+1] not in precedence.keys() and regex[i+1]!= ")":
                if regex[i] == "*":
                    newRegex += regex[i]
                    newRegex += "."
                elif regex[i] == "?":
                    newRegex += regex[i]
                    newRegex += "."
                elif regex[i] == "+":
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
    
    #print(regex)
    #convertir infix postfix
    count = 0
    for i in regex:
        #print(i)

        if i in precedence.keys() or i=="(" or i == ")":
            if len(operatorStack) > 1 and operatorStack[-1]==")" and operatorStack[-2] == "(":
                operatorStack.pop(-1)
                operatorStack.pop(-1)
                            
            if len(operatorStack)==0 or operatorStack[-1]=="(" or i == "(":
                operatorStack.append(i)
            
            elif i == ")":
                check = ""
                while check!="(":
                    postfixString += operatorStack.pop()
                    check = operatorStack[-1]
                operatorStack.pop()
                
            elif precedence[i] < precedence[operatorStack[-1]]:
                
                while precedence[i] <= precedence[operatorStack[-1]]:
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
        
        count +=1
            
        #print("stack: ", operatorStack, "string: ", postfixString)
    while len(operatorStack)!=0:
        postfixString += operatorStack.pop()
    
    #print(postfixString.replace(".", "*").replace("|", "+"))
    return postfixString


def CatchErrors(regex: str):
    operadores = ["|","*","+",".","?"]
    if not regex:
        return False
    
    if regex[0] in operadores:
        return False
 
#InfixPostfix("(↔→↓)|(↔→↓)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9)|(0|1|2|3|4|5|6|7|8|9)+|(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)((A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)|(0|1|2|3|4|5|6|7|8|9))*|(0|1|2|3|4|5|6|7|8|9)+(▪(0|1|2|3|4|5|6|7|8|9)+)?(ε(＋|-)?(0|1|2|3|4|5|6|7|8|9)+)?")

#(a|b)c
#(a|bc
#(a|b)