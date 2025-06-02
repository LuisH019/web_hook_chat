import socket

def getMachineIp ():
    try:
        hostName = socket.gethostname()
        
        ip = socket.gethostbyname(hostName)

        return ip
    
    except socket.gaierror as e:
        return f"Erro ao tentar localizar o host pelo nome: {e}"