import os

from utils.input_plus import inputPlus
from utils.network import getMachineIp

from core.setup import SetupChats

def menu():
    os.system('cls')

    print("===== MENU =====")
    print("Onde irao rodar os chats?")
    print("Escolha: ")
    print("1. Na mesma maquina")
    print("2. Em maquinas diferentes")
    print("0. Sair")
    op = inputPlus("Digite: ", 0, 2)

    os.system('cls')

    if op:
        print("Seu IP é: ", getMachineIp())

        sharedSecret = input("Digite o segredo compartilhado: ")
        myName = input("Digite seu nome: ")
        peerName = input("Digite o nome do remetente: ")

        myPort = int(input("Digite a porta onde vai rodar o seu chat: "))
        peerPort = int(input("Digite a porta onde vai rodar/esta rodando o chat do remetente: "))

        if op == 1:
            peerIp = getMachineIp()
        else:
            peerIp = input("Digite o IP do remetente: ")
            
        SetupChats(op, sharedSecret, myName, myPort, peerName, peerPort, peerIp)
