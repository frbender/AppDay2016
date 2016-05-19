from time import sleep

from Communication.CommunicationManager_old import CommunicationManager

frank = None
adrian = None
try:
    frank = CommunicationManager("FRANK", False, "139.30.136.211", "MASTER", ("139.30.136.211", 50000))
    sleep(1)
    adrian = CommunicationManager("ADRIAN", False, "139.30.136.211", "MASTER", ("139.30.136.211", 50000))
    sleep(1)

    frank.subscribe("MASTER")
    adrian.subscribe("MASTER")

    sleep(5)

    frank.sendMessage("Hallo, ich bin Frank!", "MASTER")
    adrian.sendMessage("Hallo, ich bin Adrian!", "MASTER")

except KeyboardInterrupt:
    frank.unsubscribe("MASTER")
    adrian.unsubscribe("MASTER")

    frank.networkManager.close()
    adrian.networkManager.close()