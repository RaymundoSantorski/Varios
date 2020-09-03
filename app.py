def potencia(base, potencia):
    resultado=1
    for i in range(potencia): 
        resultado=resultado*base
    return resultado

print(potencia(3,3))