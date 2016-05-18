import select
import socket
import threading


class Server(threading.Thread):
    clients = []
    senddict = dict()
    Lock = threading.Lock()

    def __init__(self, addr: (str, int), delegate):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen(1)
        self._stopme = threading.Event()
        self.delegate = delegate

    def run(self):
        try:
            while not self.stopped():
                Server.Lock.acquire()
                lesen, schreiben, oob = select.select([self.server] + Server.clients, Server.clients, [], 0.5)
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
                            self.delegate.handleNewRawMessage(nachricht.decode(), ip)
                        else:
                            print("Verbindung zu {} beendet".format(ip))
                            sock.close()
                            Server.clients.remove(sock)
                            if sock in schreiben:
                                schreiben.remove(sock)
                for sock in schreiben:
                    ip = sock.getpeername()[0]
                    if ip in Server.senddict:
                        sock.sendall(bytes(Server.senddict.pop(ip), 'utf-8'))
                if len(Server.senddict) > 0:
                    print("Not all messages send!")
                Server.Lock.release()
        finally:
            print("Closing all clients")
            for c in Server.clients:
                c.close()
            self.server.close()

    def stop(self):
        self._stopme.set()

    def stopped(self):
        return self._stopme.isSet()

    def send(self, ip : str, message : str):
        Server.Lock.acquire()
        Server.senddict[ip] = message
        Server.Lock.release()

# s = Server(("",50000))
# s.start()
# try:
#     while len(s.clients) == 0:
#         sleep(1)
#
#     print("verbunden")
#
#     s.send(s.clients[0].getpeername()[0], "Erste")
#     sleep(5)
#     s.send(s.clients[0].getpeername()[0], "Zweite")
#
#     eingabe = input("> ")
#
#     while eingabe != "ende":
#         print("...")
#         sleep(1)
#
#
# finally:
#     s.stop()
#     s.join()