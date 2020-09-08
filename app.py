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

def im_par(n):
    return n%2 == 0

def raiz_cuad(n):
    valorInicial = 0
    i = 0
    while potencia(i, 2) < n:
        i+=1
    if n-potencia(i,2) < potencia(i+1,2)-n:
        valorInicial = i
    else:
        valorInicial = i+1
    for q in range(4):
        valorInicial = (valorInicial+(n/valorInicial))/2 
    return valorInicial

def raiz_cub(n):
    valorInicial=0
    i=0
    while potencia(i,3)<n:
        i+=1
    if n-potencia(i,3) < potencia(i+1,3)-n:
        valorInicial=i
    else:
        valorInicial=i+1
    for q in range(20):
        valorInicial=(valorInicial+(n/potencia(valorInicial,2)))/2
    return valorInicial

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
        n = int(input("¿Cuantos numeros perfectos? "))
        perfectos(n)
    elif opc == "Par":
        n=int(input("Dame el numero "))
        print(im_par(n))
    elif opc == "Raiz":
        n=int(input("Dame el número "))
        print(raiz_cuad(n))
    elif opc == "Cub":
        n=int(input("Dame el numero "))
        print(raiz_cub(n))

elec()