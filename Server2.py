import socket
import select
import threading


class Server(threading.Thread):
    clients = []

    def __init__(self, addr : (str,int)):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(addr)
        self.server.listen(1)

    def run(self):
        global clients
        try:
            while True:
                lesen, schreiben, oob = select.select([server] + clients, [], [])
                for sock in lesen:
                    if sock is server:
                        client, addr = server.accept()
                        clients.append(client)
                        print("Client {} verbunden".format(addr[0]))
                    else:
                        nachricht = sock.recv(1024)
                        ip = sock.getpeername()[0]
                        if nachricht:
                            print("[{}] {}".format(ip, nachricht.decode()))
                        else:
                            print("Verbindung zu {} beendet".format(ip))
                            sock.close()
                            clients.remove(sock)
        finally:
            for c in clients:
                c.close()
            server.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 50000))
server.listen(1)

