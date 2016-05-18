import time
from threading import Thread

from Client import Client
from ProtocolHandler import ProtocolHandler
from Server import Server


class CommunicationManager:
    def __init__(self, pseudonym="NPHAERTER", isMaster=False, masterip="123.123.123.123", addr=("foobar", 1337)):

        self.isMaster = isMaster

        if not isMaster:
            self.networkManager = Client(addr)
            self.recieveThread = Thread(target=self.checkForNewPackets)
        else:
            self.networkManager = Server(addr, self)
            self.networkManager.start()

        self.protocolHandler = ProtocolHandler(pseudonym, self.networkManager, self, masterip)
        if not isMaster:
            self.recieveThread.start()
        print(
            "[CommunicationManager.__init__] Created new CommunicationManager for pseudonym \"{}\" (isMaster={})".format(
                pseudonym, isMaster))

    def checkForNewPackets(self):
        while self.networkManager.isConnectionAlive():
            msg = self.networkManager.recv()
            if msg:  # Got new messages
                self.protocolHandler.handle(msg, self.networkManager.addr[0])
            time.sleep(1)

    def handleNewRawMessage(self, messagetext, sender):
        self.protocolHandler.handle(messagetext, sender)

    def handleNewMessage(self, messagetext):
        print("[CommunicationManager.handleNewMessage] Did receive new message (\"{}\")".format(messagetext))

    def sendMessage(self, message, receiver):
        self.protocolHandler.sendMessage(message, receiver)


master = CommunicationManager("MASTER", True, "127.0.0.1", ("", 50000))
time.sleep(1)
slave = CommunicationManager("SLAVE", False, "127.0.0.1", ("127.0.0.1", 50000))
time.sleep(1)
slave.sendMessage("Meine Nachricht", "MASTER")
