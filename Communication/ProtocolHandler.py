class ProtocolMessage:
    def __init__(self, m_from="", m_to="", m_type="", m_content="", m_ip=""):
        self.m_from = m_from
        self.m_to = m_to
        self.m_type = m_type
        self.m_content = m_content
        self.m_ip = m_ip

    def __str__(self):
        return "\t".join([self.m_from, self.m_to, self.m_type, self.m_content])


class ServerProtocolHandler:
    def __init__(self, communicationmanager, networkmanager):
        self.lookuptable = {}
        self.communicationmanager = communicationmanager
        self.networkmanager = networkmanager

    def handle(self, messagestring: str, ip: str):
        parts = messagestring.split("\t")
        if len(parts) != 4:
            print("Wrong number of things in msg")

        message = ProtocolMessage(parts[0], parts[1], parts[2], parts[3], ip)

        if message.m_type == "SUBSCRIBE":
            self.handleSubscribe(message)
        elif message.m_type == "UNSUBSCRIBE":
            self.handleUnsubscribe(message)
        elif message.m_type == "MESSAGE":
            self.handleMessage(message)

    def handleSubscribe(self, message: ProtocolMessage):
        if message.m_from in self.lookuptable:
            print("already in table")
        else:
            self.lookuptable[message.m_from] = message.m_ip

    def handleUnsubscribe(self, message: ProtocolMessage):
        if message.m_from in self.lookuptable:
            del self.lookuptable[message.m_from]
        else:
            print("Not in table")

    def handleMessage(self, message: ProtocolMessage):
        if message.m_to == "MASTER":
            self.communicationmanager.handleMessageForMe(message)
        elif message.m_to == "ALL":
            for client in self.lookuptable:
                self.sendMessage(ProtocolMessage(message.m_from, client, message.m_type, message.m_content,
                                                 self.lookuptable[client]))
        elif message.m_to in self.lookuptable:
            self.sendMessage(
                ProtocolMessage(message.m_from, message.m_to, message.m_type, message.m_content,
                                self.lookuptable[message.m_to]))

    def sendMessage(self, message):
        self.networkmanager.send(message.m_ip, str(message))


class ClientProtocolHandler:
    def __init__(self, nickname, communicationmanager, networkmanager):
        self.nickname = nickname
        self.communicationmanager = communicationmanager
        self.networkmanager = networkmanager

    def handle(self, messagestring: str, ip: str):
        parts = messagestring.split("\t")
        if len(parts) != 4:
            print("Wrong number of things in msg")

        message = ProtocolMessage(parts[0], parts[1], parts[2], parts[3], ip)

        if message.m_type == "MESSAGE":
            self.handleMessage(message)
        else:
            print("Bad format")

    def handleMessage(self, message: ProtocolMessage):
        if message.m_to == self.nickname:
            self.communicationmanager.handleMessageForMe(message)
        else:
            print("Message not for me")

    def sendMessage(self, message: str):
        self.networkmanager.send(self.communicationmanager.master[0],
                                 str(ProtocolMessage(self.nickname, "MASTER", "MESSAGE", message)))

    def sendSubscribe(self):
        self.networkmanager.send(self.communicationmanager.master[0],
                                 str(ProtocolMessage(self.nickname, "MASTER", "SUBSCRIBE", "_")))

    def sendUnsubscribe(self):
        self.networkmanager.send(self.communicationmanager.master[0],
                                 str(ProtocolMessage(self.nickname, "MASTER", "UNSUBSCRIBE", "_")))
