def potencia(base, potencia):
    resultado=1
    for i in range(potencia): 
        resultado=resultado*base
    return resultado

base = int(input("Base "))
pot = int(input("Potencia "))
print("El resultado es: ",potencia(base, pot))
