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


try:
    master = CommunicationManager("MASTER", True, "127.0.0.1", ("", 50000))

    time.sleep(0.2)

    bruno = CommunicationManager("BRUNO", False, "127.0.0.1", ("127.0.0.1", 50000))
    borris = CommunicationManager("BORRIS", False, "127.0.0.1", ("127.0.0.1", 50000))

    time.sleep(1)

    bruno.subscribe("MASTER")
    time.sleep(0.5)
    borris.subscribe("MASTER")
    time.sleep(0.5)

    #    bruno.sendMessage("Meine Nachricht - in Liebe, Bruno", "MASTER")
    #    time.sleep(0.1)

    master.sendMessage("Hey :)", "ALL")
    time.sleep(1)

# master.sendClockUpdate("ALL", "13:37:42")
#    time.sleep(1)

#    borris.sendMessage("Meine Nachricht - in Liebe, Borris", "MASTER")
except KeyboardInterrupt:
    master.networkManager.stop()
    bruno.networkManager.close()
    borris.networkManager.close()
    master.networkManager.join()
