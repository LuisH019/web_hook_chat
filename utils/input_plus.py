def printErrorMessage ():
    print()
    print ("\033[91mErro: Valor Inválido!") 
    print ("\033[93mDigite novamente.")
    print("\033[0m")


def inputPlus(textoInput, min, max):
    valor = 0
    while True:
        try:
            valor = float (input(textoInput))
        except ValueError:
            printErrorMessage()
        else:
            if valor < min or valor > max:
                printErrorMessage()
            else:
                break
    
    return valor