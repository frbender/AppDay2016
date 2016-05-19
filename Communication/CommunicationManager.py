import time
from threading import Thread

from Communication.Client import Client
from Communication.ProtocolHandler import *
from Communication.Server import Server


class ServerCommunicationManager:
    def __init__(self, addr: (str, int)):
        self.server = Server(addr, self)
        self.protocolhandler = ServerProtocolHandler(self, self.server)
        self.server.start()

    def handleIncommingMessage(self, messagestr: str, ip: str):
        self.protocolhandler.handle(messagestr, ip)

    def sendMessage(self, messagestr, receiver):
        self.protocolhandler.handleMessage(ProtocolMessage("MASTER", receiver, "MESSAGE", messagestr))

    def handleMessageForMe(self, message: ProtocolMessage):
        print("Yay got new message: {}".format(str(message)))


class ClientCommunicationManager:
    def __init__(self, addr: (str, int), nickname: str):
        self.client = Client(addr)
        self.protocolhandler = ClientProtocolHandler(nickname, self, self.client)
        self.clientChecker = Thread(target=self.clientChecker)
        self.clientChecker.start()
        self.master = addr[0]

    def clientChecker(self):
        while self.client.isConnectionAlive():
            msg = self.client.recv()
            if msg:  # Got new messages
                self.protocolhandler.handle(msg)
            time.sleep(0.05)

    def sendMessage(self, messagestr):
        self.protocolhandler.sendMessage(messagestr)

    def handleMessageForMe(self, message: ProtocolMessage):
        print("Yay got new message: {}".format(str(message)))

    def subscribe(self):
        self.protocolhandler.sendSubscribe()

    def unsubscribe(self):
        self.protocolhandler.sendUnsubscribe()
