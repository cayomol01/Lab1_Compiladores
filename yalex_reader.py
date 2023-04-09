def remove_comments(line):
    if "(*" in line:
        line = line[:line.index("(*")] + line[line.index("*)") + 2:]
    return line


def read_yalex(p_input):

    definitions, tokens = {}, {}
    rule_tokens = False

    with open(p_input, 'r', encoding='utf-8') as file:
        for line in file:

            # Remove comments and strip
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
                continue

            # It's a definition
            if "let " == line[:4]:
                name, definition = line[4:].split(" = ")

                definition = definition.replace("'E'", "ε").replace("\\n", "↓").replace("\\t", "→").replace("\\r", "↕").replace("\\s", "↔").replace(".","▪")


                if definition.strip()[0] == "[":
                    definition.replace("['", "").replace("']", "").split(", ")
                    # TODO tengo que ver que hacer en los espacios

                definitions[name.strip()] = definition.strip()



                continue 

            # It's the rule token header
            if "rule tokens =" == line[:13]:
                rule_tokens = True

    return definitions, tokens

def get_range(start,end):
    #print(start, end)
    return range(ord(start),ord(end)+1)

def giga_regex(pinput: str):
    definitions, tokens = read_yalex(pinput)

    transtable = str.maketrans("[]\'\"", "    ")

    for id, defi in definitions.items():

        for key, true_regex in sorted(list(definitions.items()), key=lambda x:x[0].lower(), reverse=True):
            if key in defi:
                defi = defi.replace(key, f"{true_regex}")


        if "[" in defi and "]" in defi:

            indexa = defi.index("[")
            in_brackets = defi[defi.index("[")+1:defi.index("]")]

            #print(in_brackets)


            if "''" in in_brackets:
                meme, real = in_brackets.split("''"), []
                for let in meme:
                    let = let.translate(transtable).strip()
                    if let == "":
                        let = "風"
                    real += [let]
            else:
                real = [defi]

            sprint = ""

            for i in real:
                sreg = i.translate(transtable).strip()
                if "-" in sreg and len(sreg) >= 3:
                    meme = sreg.split(" - ")
                    rango = get_range(*meme)
                    sreg = "|".join([chr(sreg) for sreg in rango])
                if sprint:
                    sprint += "|"
                sprint += sreg
                sprint = sprint.replace("+", "＋")

            defi = defi[:indexa] + "(" + sprint + ")" + defi[defi.index("]")+1:]

            #print(defi)

        definitions[id] = defi
        #print(definitions)

    gigaregex = ""
    for id, defi in definitions.items():
        if gigaregex:
            gigaregex += "|"
        gigaregex += f"{defi}"

    #print(gigaregex)

    return gigaregex

from Thompson import Thompson
from Subconjuntos import Closure, get_groups, Subconjuntos2
from TreeDFA import TreeToDFA

if __name__ == "__main__":
    reg = "風→|↓|風→|↓|AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z||01|2|3|4|5|6|7|8|9||AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|AB|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|01|2|3|4|5|6|7|8|9"
    afn = Thompson(reg)
    afd = Subconjuntos2(afn)
    afd2 = TreeToDFA(reg)
    print(afd.transitions)
    afd.ShowGraph(name="pruebas.png")
    
    