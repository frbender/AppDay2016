import time
from threading import Thread

from Client import Client
from ProtocolHandler import ProtocolHandler


class CommunicationManager:
    def __init__(self, pseudonym="NPHAERTER", isMaster=False, masterip="123.123.123.123", addr=("foobar", 1337)):
        self.isMaster = isMaster
        if not isMaster:
            self.networkManager = Client(addr)
            self.recieveThread = Thread(target=self.checkForNewPackets)
        else:
            print(
                "HOLY SHIT MOTHERF*CKER HERE SHOULD BE THE INIT-STUFF FOR THE INCREDIBLE SERVERCLASS OH YEAH VAGINA PENIS TOUCHDOOOOOWN")
        self.protocolHandler = ProtocolHandler(pseudonym, self.networkManager, self, masterip)

    def checkForNewPackets(self):
        while self.networkManager.isConnectionAlive():
            msg = self.networkManager.recv()
            if msg != "":  # Got new messages
                self.protocolHandler.handle(msg, self.networkManager.addr[0])
            time.sleep(0.2)

    def handleNewMessage(self, messagetext):
        print("Whohooo got new message: \"{}\"".format(messagetext))
