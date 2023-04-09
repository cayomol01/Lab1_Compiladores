def remove_comments(line):
    if "(*" in line:
        line = line[:line.index("(*")] + line[line.index("*)") + 2:]
    return line

#Funcion para saber si los comentarios fueron cerrados o no. 
def checkComments(line):
    if "(*" in line:
        return( "*)" in line[line.index("(*"):])
    if "*)" in line:
        return( "(*" in line[:line.index("*)")])
    else:
        return True
    
def inBrackets(string):
    if string[0] == "[" and string[-1]== "]":
        return True
    elif string[0] == "(" and string[-1] == ")":
        return True
    return False
def checkLetStructure(line):
    #Eliminar espacios en blanco antes y después. 
    line = line.strip()
    if "let" in line[:3]:

        if line[3:][0] !=" ":
            #print("error de caracter despues de let")

            return False
        
        after_let = line[3:]
        
        name, definition = after_let.split("=")
        name = name.strip()
        definition = definition.strip()

        
        
        if len(name.split(" "))>1:
            #print("error de mas de un string en el puesto de nombre")

            return False
        if checkComments(definition):
            definition = remove_comments(definition).strip()
            if inBrackets(definition):
                if len(definition[:definition.index("[")]) >0:
                    return False
            else:
                if len(definition.split(" ")) > 1:
                    #print("error de mas de un string en el puesto de definition")
                    return False
        return True
    else:
        return False
        


def read_yalex_rules(filename):
    errors = []
    line_counter = 1
    definitions, tokens = {}, {}
    rule_tokens = False

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove comments and strip
            if checkComments(line)==False:
                errmess = f"Error en la línea {line_counter}. Comentario mal definido"
                errors.append(errmess)

            else:
                line = remove_comments(line.strip())


            # It's a token
            if rule_tokens:
                if line == "":
                    break # End of tokens, we can stop

                if "|" == line[:1]:
                    line = line[2:]

                if " {" in line:
                    token, function = line.split(" {")
                else:
                    token = line
                    function = "None"

                tokens[token.strip()] = function.replace("return", "").replace("}", "").strip()
                line_counter+=1
                continue
            
            if "rule tokens =" == line[:13]:
                rule_tokens = True
                continue

            # It's a definition
            if "let" in line.split("=")[0].split(" ")[0]:
                if checkLetStructure(line):
                    name, definition = line[4:].split(" = ")
                    definition = definition.replace("'E'", "ε").replace("\\n", "↓").replace("\\t", "→").replace("\\r", "↕").replace("\\s", "↔").replace(".","▪")

                    if definition.strip()[0] == "[":
                        definition.replace("['", "").replace("']", "").split(", ")
                        # TODO tengo que ver que hacer en los espacios

                    definitions[name.strip()] = definition.strip()
                    line_counter+=1

                    continue
                else:
                    errmess = f"Error en la línea {line_counter}. La estructura del let no es correcta."
                    errors.append(errmess)
                    line_counter+=1
                    continue
                    
                
            line_counter+=1

            # It's the rule token header

    if errors:
        for i in errors:
            print(i)
        return None
    return definitions, tokens


def get_range(start, end):
    return range(ord(start), ord(end) + 1)


def build_regex(filename):
    if read_yalex_rules(filename):
        definitions, tokens = read_yalex_rules(filename)
        transtable = str.maketrans("[]\'\"", "    ")
        

        for name, definition in definitions.items():
            for key, true_regex in sorted(list(definitions.items()), key=lambda x:x[0].lower(), reverse=True):
                if key in definition:
                    definition = definition.replace(key, f"{true_regex}")

            if "[" in definition and "]" in definition:
                indexa = definition.index("[")
                in_brackets = definition[definition.index("[")+1:definition.index("]")]

                if "''" in in_brackets:
                    split_regex, final_regex = in_brackets.split("''"), []
                    for char in split_regex:
                        char = char.translate(transtable).strip()
                        if char == "":
                            char = "@"
                        final_regex += [char]
                else:
                    final_regex = [definition]

                regex_str = ""
                for regex_part in final_regex:
                    sanitized_regex = regex_part.translate(transtable).strip()
                    if "-" in sanitized_regex and len(sanitized_regex) >= 3:
                        split_range = sanitized_regex.split(" - ")
                        char_range = get_range(*split_range)
                        sanitized_regex = "|".join([chr(char) for char in char_range])
                    if regex_str:
                        regex_str += "|"
                    regex_str += sanitized_regex
                    regex_str = regex_str.replace("+", "＋")

                definition = definition[:indexa] + "(" + regex_str + ")" + definition[definition.index("]")+1:]

            definitions[name] = definition

        full_regex = ""
        for name, definition in definitions.items():
            if full_regex:
                full_regex += "|"
            full_regex += f"{definition}"

        return full_regex
    else:
        return None


from Thompson import Thompson
from Subconjuntos import Closure, get_groups, Subconjuntos2
from TreeDFA import TreeToDFA

if __name__ == "__main__":
    file = "yalex/slr-3.yal"
    if build_regex(file):
        reg = build_regex(file)
        print(reg)
        #afn = Thompson(reg)
        #afn.ShowGraph2(name="outputs/a3")
    
        
    