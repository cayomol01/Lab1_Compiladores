from yalex import Lexer

lexer = Lexer()
lexer.load('yalex/slr-1.yal')
for token in lexer.tokenize('input string'):
    print(token)