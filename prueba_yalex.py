def read_yalex(p_input):
    definitions, tokens = {}, {}
    rule_tokens = False
    regex = ""

    with open(p_input, 'r', encoding='utf-8') as file:
        for line in file:

            # Remove comments and strip
            if "(*" in line:
                line = line[:line.index("(*")] + line[line.index("*)") + 2:]
            line = line.strip()

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
                definition = definition.replace("'", "")
                definitions[name.strip()] = definition.strip()
                continue 

            # It's the rule token header
            if "rule tokens =" == line[:13]:
                rule_tokens = True

        # Generate the regular expression
        for id, defi in definitions.items():
            regex += defi

        regex = regex.replace("[", "(").replace("]", ")").replace("|)", ")")
        regex = f"({regex})"

        for token, function in tokens.items():
            regex = regex.replace(token, function)

    return regex

if __name__ == "__main__":
    print(read_yalex("yalex/slr-1.yal"))