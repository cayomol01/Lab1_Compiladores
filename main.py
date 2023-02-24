from Thompson import Thompson

if __name__=="__main__":
    s = "ab*ab*"
    
    prueba = Thompson(s)
    prueba.getInfo()
    for key, value in prueba.trans_symbols.items():
        print(key,value)
    for key, value in prueba.Transiciones().items():
        print(key,value)
        
    prueba.ShowGraph()
 
    print(" ")