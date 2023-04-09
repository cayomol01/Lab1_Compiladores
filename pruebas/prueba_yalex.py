


def hola(string):
    if "a" in string:
        raise "Error"
    else:
        return "good"
    
def bola(string):
    h = hola(string)
    return h+h


h = "hola  adios"
print(h.split(" "))
