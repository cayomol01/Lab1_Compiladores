from Thompson import Thompson
from Subconjuntos import Closure, get_groups, Subconjuntos2
from TreeDFA import TreeToDFA
from yalex_reader import build_regex
from Afd import AFD
from Automata import Automata

if __name__ == "__main__":
    file = "./yalex/s1.yal"
    if build_regex(file):
        reg = build_regex(file)
        with open('pruebas/generated.py', 'w', encoding="utf-8") as file:
            file.write("from Afd import AFD\n")
            file.write("from Thompson import Thompson\n")
            file.write("\n")
            file.write(f"reg = '{reg}'\n")
            file.write(f"afn = Thompson(reg)\n")
            file.write("txt_input = 'input.txt'\n")
            file.write("lines = []\n")
            file.write("tokens = []\n")
            file.write("\n")
            file.write("with open('pruebas/input.txt', 'r', encoding='utf-8') as file:\n")
            file.write("\tlines = file.readlines()\n")
            file.write("\n")
            file.write("lines = [i.strip() for i in lines]\n")
            file.write("errors = []\n")
            file.write("\n")
            file.write("for i in range(len(lines)):\n")
            file.write("\tif afn.simulate2(lines[i]) == False:\n")
            file.write("\t\terrors.append(f'Syntax error on line {i} -> {lines[i]}')\n")
            file.write("\telse:\n")
            file.write("\t\ttokens.append(lines[i])\n")
            file.write("\n")
            file.write("if errors:\n")
            file.write("\tfor i in errors:\n")
            file.write("\t\tprint(i)\n")
            file.write("else:\n")
            file.write("\tprint('Program has no syntax errors')\n")
            file.write("\tfor i in tokens:\n")
            file.write("\t\tprint('token: ', i)\n")
        
        
    
        #file.write("from Afd import AFD\n")
        #file.write("from Afd import AFD\n")
        #file.write("from Afd import AFD\n")

        #↔→.↓.(↔→↓)
        #print(reg)
        #reg = "(a|b|c)"
        #print(reg)
        #(↔*→*↓)+(↔*→*↓)+(A+B+C+D)*#
        #reg = "(↔→↓)|(↔→↓)+|(A|B|C|D)"
        #afd = TreeToDFA(reg)
        #afd2 = TreeToDFA(reg2)
        #afn = Thompson(reg)
        
        #afd.ShowGraph2(name="outputs/prueba")
        #afd2 = Thompson(reg)
        
        #print(afd2.simulate2('ab'))
    
    #automata.ShowGraph()
    #print("transitions: ", afd.transitions)
    #print("start_state: ", afd.start)
    #print("acceptance_states", afd.final)
    #print(afd.simulate("acc"))
    
    #minimized_afd = afd.minimize()
#
    #print("transitions: ", minimized_afd.transitions)
    #print("start_state: ", minimized_afd.start)
    #print("acceptance_states", minimized_afd.final)
    #
    #minimized_afd.ShowGraph()
