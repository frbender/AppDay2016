import time

from CommunicationManager import CommunicationManager

try:
    master = CommunicationManager("MASTER", True, "127.0.0.1", "MASTER", ("", 50000))

    time.sleep(1)

    borris = CommunicationManager("BORRIS", False, "127.0.0.1", "MASTER", ("127.0.0.1", 50000))

    time.sleep(1)

    borris.subscribe("MASTER")

    time.sleep(1)

    master.sendMessage("Hallo, hier ist Master", "ALL")

    time.sleep(1)

    master.sendMessage("Moin Moin", "BORRIS")

    time.sleep(1)

    borris.sendMessage("Meine Nachricht - in Liebe, Borris", "MASTER")

except KeyboardInterrupt:
    master.networkManager.stop()
    # bruno.networkManager.close()
    borris.networkManager.close()
    master.networkManager.join()
