import time
from threading import Thread

from Client import Client
from ProtocolHandler import ProtocolHandler
from Server import Server


class CommunicationManager:
    debug = True
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
        if self.debug:
            print(
            "[CommunicationManager.__init__] <{}> Created new CommunicationManager for pseudonym \"{}\" (isMaster={})".format(
                pseudonym, pseudonym, isMaster))

    def checkForNewPackets(self):
        while self.networkManager.isConnectionAlive():
            msg = self.networkManager.recv()
            if msg:  # Got new messages
                self.protocolHandler.handle(msg, self.networkManager.addr[0])
            time.sleep(0.2)

    def handleNewRawMessage(self, messagetext, sender):
        self.protocolHandler.handle(messagetext, sender)

    def handleNewMessage(self, messagetext):
        if self.debug:
            print("[CommunicationManager.handleNewMessage] <{}> Did receive new message (\"{}\")".format(
            self.protocolHandler.pseudonym, messagetext))

    def sendMessage(self, message, receiver):
        if self.debug:
            print("[CommunicationManager.sendMessage] <{}> Will send Message \"{}\" to \"{}\"".format(
                self.protocolHandler.pseudonym, message, receiver))
        self.protocolHandler.sendMessage(message, receiver)

    def subscribe(self, reciever):
        self.protocolHandler.sendSubscribe(reciever)

    def unsubscribe(self, reciever):
        self.protocolHandler.sendUnsubscribe(reciever)

    def sendClockUpdate(self, reciever, clockupdate):
        self.protocolHandler.sendClockUpdate(reciever, clockupdate)

    def handleClockUpdate(self, clockupdate):
        if self.debug:
            print("[CommunicationManager.handleClockUpdate] <{}> Did receive clock update \"{}\")".format(
                self.protocolHandler.pseudonym, clockupdate))
