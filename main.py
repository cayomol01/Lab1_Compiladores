from Thompson import Thompson

if __name__=="__main__":
    s = "0?(1?)?0+"

    prueba = Thompson(s)
    prueba.ShowGraph()