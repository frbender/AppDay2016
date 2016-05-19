class ProtocolMessage:
    def __init__(self, m_from="", m_to="", m_type="", m_content="", m_sender=""):
        self.m_from = m_from
        self.m_to = m_to
        self.m_type = m_type
        self.m_content = m_content
        self.m_sender = m_sender

    def __str__(self):
        return "\t".join([self.m_from, self.m_to, self.m_type, self.m_content])


class ProtocolHandler:
    debug = True
    pseudonym = "BLA"
    masterip = "123.123.123.123"
    masterpsd = "123.123.123.123"
    lookuptable = {}
    networtManager = object()
    communicationManager = object()

    def __init__(self, pseudonym, networkManager, communicationManager, masterip="", masterpsd=""):
        self.pseudonym = pseudonym
        self.networtManager = networkManager
        self.communicationManager = communicationManager
        self.masterip = masterip
        self.masterpsd = masterpsd
        self.lookuptable[masterpsd] = masterip

    # message = raw message
    # sender = ip address of sender of message
    def handle(self, message: str, sender: str):
        parts = message.split('\t')
        if not len(parts) in [3, 4]:
            print("[ProtocolManager.handle] <{}> Handled Message is bad :( (\"{}\")".format(self.pseudonym, message))
            return
        messageobject = ProtocolMessage(parts[0], parts[1], parts[2], parts[3], sender)

        if messageobject.m_type == "SUBSCRIBE":
            self.handleSubscribe(messageobject)
        elif messageobject.m_type == "UNSUBSCRIBE":
            self.handleUnsubscribe(messageobject)
        elif messageobject.m_type == "CLOCKUPDATE":
            self.handleClockUpdate(messageobject)
        elif messageobject.m_type == "MESSAGE":
            self.handleMessage(messageobject)

    def handleSubscribe(self, message: ProtocolMessage):
        if not message.m_from in self.lookuptable:
            self.lookuptable[message.m_from] = message.m_sender
            if self.debug:
                print("[ProtocolManager.handleSubscribe] <{}> Added \"".format(
                    self.pseudonym) + message.m_from + "\" <" + message.m_sender + "> to lookuptable")
        else:
            print(
                "[ProtocolManager.handleSubscribe] <{}> Recieved \"SUBSCRIBE\"-Message from \"".format(
                    self.pseudonym) + message.m_from + "\" <" + message.m_sender + "> but already in lookuptable so I won't care")

    def handleUnsubscribe(self, message: ProtocolMessage):
        if message.m_from in self.lookuptable:
            del self.lookuptable[message.m_from]
            if self.debug:
                print(
                "[ProtocolManager.handleUnsubscribe] <{}> Removed \"".format(
                    self.pseudonym) + message.m_from + "\" <" + message.m_sender + "> from lookuptable")
        else:
            print(
                "[ProtocolManager.handleSubscribe] <{}> Recieved \"UNSUBSCRIBE\"-Message from \"".format(
                    self.pseudonym) + message.m_from + "\" <" + message.m_sender + "> but not found in lookuptable so I won't care")

    def handleClockUpdate(self, message: ProtocolMessage):
        self.communicationManager.handleClockUpdate(message.m_content)

    def handleMessage(self, message: ProtocolMessage):
        if self.debug:
            print("[ProtocolManager.handleMessage] <{}> Recieved \"MESSAGE\"-Message (in general) \"".format(
                self.pseudonym) + str(
            message) + "\"")
        if message.m_to == self.pseudonym:
            self.communicationManager.handleNewMessage(message.m_content)
            return
        if message.m_to == "ALL":
            if self.debug:
                print("[ProtocolManager.handleMessage] <{}> Handling \"MESSAGE\"-Message for all \"".format(
                    self.pseudonym) + str(message) + "\"")
                print("[ProtocolManager.handleMessage] <{}> Current Lookup-Table: {}".format(self.pseudonym,
                                                                                             str(self.lookuptable)))
            for client in self.lookuptable:
                if not client == message.m_to and not client == self.masterpsd:
                    self.networtManager.send(self.lookuptable[client], str(
                        ProtocolMessage(message.m_from, client, "MESSAGE", message.m_content)))
            return
        # Müll
        if message.m_to in self.lookuptable:
            self.networtManager.send(self.lookuptable[message.m_to],
                                     str(ProtocolMessage(message.m_from, message.m_to, "MESSAGE", message.m_content)))

    def sendMessage(self, message, receiver):
        print("[ProtocolManager.sendMessage] <{}> Redirecting to handleMessage...".format(self.pseudonym))
        self.handleMessage(ProtocolMessage(self.pseudonym, receiver, "MESSAGE", message))

    def sendSubscribe(self, receiver):
        if self.debug:
            print("[ProtocolHandler.sendSubscribe] <{}> Will send Subscribe to \"{}\"".format(
                self.pseudonym, receiver))

        self.networtManager.send(self.masterip, str(ProtocolMessage(self.pseudonym, receiver, "SUBSCRIBE", "")))

    def sendUnsubscribe(self, receiver):
        if self.debug:
            print("[ProtocolHandler.sendUnsubscribe] <{}> Will send Unsubscribe to \"{}\"".format(
                self.pseudonym, receiver))

        self.networtManager.send(self.masterip, str(ProtocolMessage(self.pseudonym, receiver, "UNSUBSCRIBE", "")))

    def sendClockUpdate(self, receiver, clockupdate):
        if receiver in self.lookuptable:
            self.networtManager.send(self.lookuptable[receiver],
                                     str(ProtocolMessage(self.pseudonym, receiver, "CLOCKUPDATE", clockupdate)))

# Beispiele für den ProtocolHandler
# ph = ProtocolHandler("Mein Pseudonym", object(), object(), "MASTER", "123.123.123.123")
# 1: lokales Pseudonym -> is klar
# 2: networkHandler -> muss "send(ip-adresse, nachricht)" bereitstellen
# 3: communicationManager -> muss handleNewMessage(textmessage)
# 4: masterip -> ip des masters
#
# Benutzung
# Muss von communicationManager erstellt werden. handle muss aufgerufen werden, sobald eine
# neue nachricht vom server/client reinkommt. sendMessage kann von einem Client aufgerufen werden,
# der an den Master senden will. auch der master kann das benutzen, indem er sozusagen eine nachricht
# an sich selbst sendet sendMessage(message, "ALL") (->sendet an sich selbst nachricht, die dann an alle
# verteilt wird)
