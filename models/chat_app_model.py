import requests
import threading
import datetime
import logging
import time
from flask import Flask, redirect, url_for, jsonify, render_template, request
from utils.cryptography.my_rsa import rsaGenerateKeys, rsaEncode, rsaDecode
from utils.cryptography.my_hmac import hmacGenerateKey, hmacEncodeSha256
from utils.network import getMachineIp

class ChatAppModel:
    def __init__(self, sharedSecret, myName, myPort, peerName, peerPort, peerIp=getMachineIp()):
        self.app = Flask(__name__, template_folder = '../templates', static_folder = "../static")
        
        self.sharedSecret = sharedSecret
        self.myName = myName
        self.myPort = myPort
        self.peerName = peerName
        self.peerPort = peerPort
        self.peerIp = peerIp
        
        self.allMessages = []
        
        
        self.myPublicKey, self.myPrivateKey = rsaGenerateKeys()
        self.peerPublicKey = None

        self.myHmacKey = None
        self.peerHmacKey = None

        self.myKeysSent = False

        self.setupLogging()
        self.setupRoutes()

    def setupLogging(self):
        self.logger = logging.getLogger(f'ChatApp_{self.myName}')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setupRoutes(self):
        self.app.route('/')(self.home)
        self.app.route('/registerPeerKey', methods=['POST'])(self.registerPeerKey)
        self.app.route('/webhook', methods=['POST'])(self.receiveMessage)
        self.app.route('/send', methods=['POST'])(self.sendMessage)
        self.app.route('/messages')(self.listMessages)
    
    def home(self):
        self.sendPublicKey()
        return render_template('app.html')
    
    def sendPublicKey(self):
        if not self.myKeysSent or len(self.allMessages) % 50 == 0:
            try:
                self.myHmacKey = hmacGenerateKey(256)

                requests.post(f"http://{self.peerIp}:{self.peerPort}/registerPeerKey", 
                              json={
                                  "publicKey": self.myPublicKey,
                                  "hmacKey": self.myHmacKey,
                                  })

                self.myKeysSent = True

                self.logger.info("Chave pública e HMAC enviada para %s com sucesso", self.peerName)

                return '', 200
            except Exception as e:
                self.logger.error("Erro ao registrar chave pública e HMAC em %s: %s", self.peerName, str(e))

                return '', 400
        else:
            self.logger.info("Chave pública e HMAC já enviada para %s", self.peerName)

            return '', 200

    def registerPeerKey(self):
        try:           
            self.peerPublicKey = request.json['publicKey']
            self.peerHmacKey = request.json['hmacKey']

            self.logger.info("Chave pública e HMAC de %s registrada com sucesso", self.peerName)    
        
            return '', 200
        except Exception as e:
            self.logger.error("Erro ao registrar chave pública e HMAC de %s: %s", self.peerName, str(e))

            return '', 400
        
    def sendMessage(self):
        if request.method == 'POST':
            messageText = request.form['message']
        
            def sendAsync():
                try:
                    messageContent = {
                        "message": messageText,
                        "sender": "Eu",
                        "receiver": self.peerName,
                        "datetime": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
                    }

                    self.allMessages.append(messageContent)
                    
                    hmacMessage = hmacEncodeSha256(messageText + self.sharedSecret, self.myHmacKey)
                    cypherText = rsaEncode(messageText, self.peerPublicKey)

                    encondedMessageContent = {
                        "message": cypherText,
                        "sender": self.myName,
                        "receiver": self.peerName,
                        "datetime": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")),
                        "hmacMessage": hmacMessage
                    }

                    requests.post(f"http://{self.peerIp}:{self.peerPort}/webhook", json=encondedMessageContent, timeout = 2)

                    self.logger.info("Mensagem enviada para %s", self.peerName)
                except Exception as e:
                    self.logger.error("Erro ao enviar mensagem: %s", str(e))

            thread = threading.Thread(target=sendAsync)
            thread.start()
        
        return redirect(url_for('home'))
    
    def receiveMessage(self):
        try:
            if not self.peerPublicKey or not self.peerHmacKey:
                self.logger.error("Chave pública ou HMAC do peer não registrada.")
                return '', 400
            else:
                cypherText = request.json['message']
                decryptedMessage = rsaDecode(cypherText, self.myPrivateKey)

                if request.json['hmacMessage'] != hmacEncodeSha256(decryptedMessage + self.sharedSecret, self.peerHmacKey):
                    self.logger.error("HMAC inválido recebido de %s", self.peerName)
                    return '', 400
                else:
                    receivedMessage = {
                        "sender": self.peerName,
                        "receiver": "Eu",
                        "message": decryptedMessage,
                        "datetime": request.json['datetime']
                    }

                    self.allMessages.append(receivedMessage)

                    self.logger.info("Mensagem recebida de %s", self.peerName)

                    return '', 200
        except Exception as e:
            self.logger.error("Erro ao receber mensagem: %s", str(e))

            return '', 400

    def listMessages(self):
        return jsonify(self.allMessages)

    def run(self):
        self.app.run(host="0.0.0.0", port=self.myPort)

    