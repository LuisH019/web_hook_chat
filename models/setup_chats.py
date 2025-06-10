from multiprocessing import Process

from models.chat_app_model import ChatAppModel

class SetupChats():
    def __init__(self, op, sharedSecret, myName, myPort, peerName, peerPort, peerIp):
        self.op = op
        self.sharedSecret = sharedSecret

        self.myName = myName
        self.myPort = myPort

        self.peerName = peerName
        self.peerPort = peerPort
        self.peerIp = peerIp

        if op == 1:
            self.initProcesses()
        else:
            self.runChatA()

    def runChatA(self):
        chatA = ChatAppModel(sharedSecret=self.sharedSecret, myName=self.myName, myPort=self.myPort, peerName=self.peerName, peerPort=self.peerPort)
        chatA.run()

    def runChatB(self):
        chatB = ChatAppModel(sharedSecret=self.sharedSecret, myName=self.peerName, myPort=self.peerPort, peerName=self.myName, peerPort=self.myPort)
        chatB.run()

    def initProcesses(self):
        processA = Process(target=self.runChatA)
        processB = Process(target=self.runChatB)

        processA.start()
        processB.start()

        processA.join()
        processB.join()
