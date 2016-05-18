import sys


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
    pseudonym = "MASTEROFDESASTER"
    lookuptable = {}
    networtManager = object()
    communicationManager = object()

    def handle(self, message: str, sender: str):
        parts = message.split('\t')
        if len(parts) != 4:
            print("message is not correct (\"" + message + "\")", file=sys.stderr)
            return
        messageobject = ProtocolMessage(parts[0], parts[1], parts[2], parts[3])

        if messageobject.m_type == "SUBSCRIBE":
            self.handleSubscribe(messageobject)
        elif messageobject.m_type == "UNSUBSCRIBE":
            self.handleUnsubscribe(messageobject)
        elif messageobject.m_type == "MESSAGE":
            self.handleMessage(messageobject)

    def handleSubscribe(self, message: ProtocolMessage):
        if not message.m_from in self.lookuptable:
            self.lookuptable[message.m_from] = message.m_sender
            print("added \"" + message.m_from + "\" <" + message.m_sender + "> to lookuptable!")
        else:
            print(
                "recieved SUBSCRIBEmessage from \"" + message.m_from + "\" <" + message.m_sender + "> but already in lookuptable so I won't care")

    def handleUnsubscribe(self, message: ProtocolMessage):
        if message.m_from in self.lookuptable:
            del self.lookuptable[message.m_from]
            print("removed \"" + message.m_from + "\" <" + message.m_sender + "> from lookuptable!")
        else:
            print(
                "recieved UNSUBSCRIBEmessage from \"" + message.m_from + "\" <" + message.m_sender + "> but not found in lookuptable so I won't care")

    def handleMessage(self, message: ProtocolMessage):
        print("recieved MESSAGEmessage (" + str(message) + ")")
        if message.m_to == self.pseudonym:
            self.communicationManager.handleNewMessage(message)
        if message.m_to == "ALL":
            print("recieved MESSAGEmessage for all (" + str(message) + ")")
            for reciever in self.lookuptable:
                if not reciever == message.m_from:
                    self.networtManager.send(self.lookuptable[reciever], str(
                        ProtocolMessage(reciever, self.pseudonym, "MESSAGE", message.m_content)))
