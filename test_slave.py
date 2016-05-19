from CommunicationManager import CommunicationManager

frank = CommunicationManager("FRANK", False, "139.30.136.211", ("139.30.136.211", 50000))
adrian = CommunicationManager("ADRIAN", False, "139.30.136.211", ("139.30.136.211", 50000))

frank.subscribe("MASTER")
adrian.subscribe("MASTER")

frank.sendMessage("Hallo, ich bin Frank!", "MASTER")
adrian.sendMessage("Hallo alle!", "ALL")