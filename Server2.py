import socket
import select
import threading
from time import sleep


class Server(threading.Thread):
    clients = []

    def __init__(self, addr : (str,int)):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen(1)
        self._stopme = threading.Event()

    def run(self):
        try:
            while not self.stopped():
                lesen, schreiben, oob = select.select([self.server] + Server.clients, [], [], 0.5)
                for sock in lesen:
                    if sock is self.server:
                        client, addr = self.server.accept()
                        self.clients.append(client)
                        print("Client {} verbunden".format(addr[0]))
                    else:
                        nachricht = sock.recv(1024)
                        ip = sock.getpeername()[0]
                        if nachricht:
                            print("[{}] {}".format(ip, nachricht.decode()))
                        else:
                            print("Verbindung zu {} beendet".format(ip))
                            sock.close()
                            Server.clients.remove(sock)
        finally:
            for c in Server.clients:
                c.close()
            self.server.close()

    def stop(self):
        self._stopme.set()

    def stopped(self):
        return self._stopme.isSet()


s = Server(("",50000))
s.setDaemon(True)
s.start()

eingabe = input("> ")
while eingabe != "ende":
    print("...")
    sleep(1)

s.stop()
s.join()
