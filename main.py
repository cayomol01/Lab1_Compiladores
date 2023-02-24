from Thompson import Thompson

if __name__=="__main__":
    s = "ab*ab*"
    
    prueba = Thompson(s)
    prueba.getInfo()
    print(prueba.edges)
    print(prueba.trans_symbols)
    prueba.ShowGraph()
    
    print(Thompson(s).Transiciones())
    print(" ")