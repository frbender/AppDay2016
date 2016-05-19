from time import sleep

from Communication.CommunicationManager import ClientCommunicationManager

max = ClientCommunicationManager(("192.168.0.101",50000), "MAX")

max.subscribe()
sleep(2)
max.sendMessage("Hallo du da tolle sache")

