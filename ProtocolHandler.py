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
    pseudonym = "BLA"
    masterip = "123.123.123.123"
    lookuptable = {}
    networtManager = object()
    communicationManager = object()

    def __init__(self, pseudonym, networkManager, communicationManager, masterip=""):
        self.pseudonym = pseudonym
        self.networtManager = networkManager
        self.communicationManager = communicationManager
        self.masterip = masterip

    # message = raw message
    # sender = ip address of sender of message
    def handle(self, message: str, sender: str):
        parts = message.split('\t')
        if not len(parts) in [3, 4]:
            print("[ProtocolManager.handle] Handled Message is bad :( (\"{}\")".format(message))
            return
        messageobject = ProtocolMessage(parts[0], parts[1], parts[2], parts[3], sender)

        if messageobject.m_type == "SUBSCRIBE":
            self.handleSubscribe(messageobject)
        elif messageobject.m_type == "UNSUBSCRIBE":
            self.handleUnsubscribe(messageobject)
        elif messageobject.m_type == "MESSAGE":
            self.handleMessage(messageobject)

    def handleSubscribe(self, message: ProtocolMessage):
        if not message.m_from in self.lookuptable:
            self.lookuptable[message.m_from] = message.m_sender
            print(
                "[ProtocolManager.handleSubscribe] Added \"" + message.m_from + "\" <" + message.m_sender + "> to lookuptable")
        else:
            print(
                "[ProtocolManager.handleSubscribe] Recieved \"SUBSCRIBE\"-Message from \"" + message.m_from + "\" <" + message.m_sender + "> but already in lookuptable so I won't care")

    def handleUnsubscribe(self, message: ProtocolMessage):
        if message.m_from in self.lookuptable:
            del self.lookuptable[message.m_from]
            print(
                "[ProtocolManager.handleUnsubscribe] Removed \"" + message.m_from + "\" <" + message.m_sender + "> from lookuptable")
        else:
            print(
                "[ProtocolManager.handleSubscribe] Recieved \"UNSUBSCRIBE\"-Message from \"" + message.m_from + "\" <" + message.m_sender + "> but not found in lookuptable so I won't care")

    def handleMessage(self, message: ProtocolMessage):
        print("[ProtocolManager.handleMessage] Recieved \"MESSAGE\"-Message \"" + str(message) + "\"")
        if message.m_to == self.pseudonym:
            self.communicationManager.handleNewMessage(message)
            return
        if message.m_to == "ALL":
            print("[ProtocolManager.handleMessage] Recieved \"MESSAGE\"-Message for all \"" + str(message) + "\"")
            for reciever in self.lookuptable:
                if not reciever == message.m_from:
                    self.networtManager.send(self.lookuptable[reciever], str(
                        ProtocolMessage(reciever, self.pseudonym, "MESSAGE", message.m_content)))
            return
        if message.m_to in self.lookuptable:
            self.networtManager.send(self.lookuptable[message.m_to],
                                     str(ProtocolMessage(message.m_to, self.pseudonym, "MESSAGE", message.m_content)))
            return

    def sendMessage(self, message, receiver):
        self.networtManager.send(self.masterip,
                                 str(ProtocolMessage(receiver, self.pseudonym, "MESSAGE", message)))

    def sendSubscribe(self, receiver):
        self.networtManager.send(self.masterip, str(ProtocolMessage(receiver, self.pseudonym, "SUBSCRIBE", "")))

    def sendUnsubscribe(self, receiver):
        self.networtManager.send(self.masterip, str(ProtocolMessage(receiver, self.pseudonym, "SUBSCRIBE", "")))


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
