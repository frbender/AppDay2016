import ProtocolHandler


class CommunicationManager:
    def __init__(self, isMaster=False):
        self.isMaster = isMaster
        self.protocolHandler = ProtocolHandler()
        if not isMaster:
            self.networkManager = Client()
