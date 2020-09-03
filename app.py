def potencia(base, potencia):
    resultado=1
    for i in range(potencia): 
        resultado=resultado*base
    return resultado

def factorial(n):
    if n==1:
        return 1
    else:
        return n*factorial(n-1)

def elec():
    opc = input("¿Factorial o Potencia?")
    if opc == "Factorial":
        fac = int(input("Número para calcular el factorial "))
        print(factorial(fac))
    elif opc == "Potencia":
        base = int(input("Base "))
        pot = int(input("Potencia "))
        print(potencia(base, pot))

elec()