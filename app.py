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

def primo(n):
    divisores=0
    for i in range(int(n/2)):
        if n%(i+1)==0:
            divisores+=1
    return divisores==1

def perfectos(n):
    for i in range(n):
        if primo(i) == True:
            if primo(potencia(2,i)-1) == True:
                perfecto = potencia(2,(i-1))*(potencia(2,i)-1)
                print(perfecto)



def elec():
    opc = input("¿Factorial, Potencia, Primo o Perfecto?")
    if opc == "Factorial":
        fac = int(input("Número para calcular el factorial "))
        print(factorial(fac))
    elif opc == "Potencia":
        base = int(input("Base "))
        pot = int(input("Potencia "))
        print(potencia(base, pot))
    elif opc == "Primo":
        n = int(input("Numero a evaluar"))
        print(primo(n))
    elif opc == "Perfecto":
        n = int(input("¿Cuantos numeros perfectos?"))
        perfectos(n)


elec()