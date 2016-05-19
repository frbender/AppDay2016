import time

from Communication.CommunicationManager import ServerCommunicationManager

master = None
try:
    master = ServerCommunicationManager(("", 50000))

    while not "MAX" in master.protocolhandler.lookuptable:
        time.sleep(0.2)

    time.sleep(4)

    master.sendMessage("Hallo mein Schatz", "ALL")
    master.sendMessage("Hallo anderer Schatz", "MAX")

except KeyboardInterrupt:
    master.server.stop()
    master.server.join()
