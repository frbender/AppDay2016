import time

from Communication.CommunicationManager_old import CommunicationManager

master = None
try:
    master = CommunicationManager("MASTER", True, "127.0.0.1", "MASTER", ("", 50000))

    while "FRANK" not in master.protocolHandler.lookuptable:
        time.sleep(0.5)
    while "ADRIAN" not in master.protocolHandler.lookuptable:
        time.sleep(0.5)

    master.sendMessage("Hallo, hier ist Master", "ALL")

    time.sleep(1)

    master.sendMessage("Moin Moin", "ADRIAN")

    time.sleep(1)

    master.sendMessage("Moin Moin", "FRANK")
    time.sleep(0.5)

    master.sendMessage("Hallo, hier ist noch ein Master", "ALL")


except KeyboardInterrupt:
    master.networkManager.stop()
    master.networkManager.join()
