import select
import socket
import threading
import time


class Server(threading.Thread):
    clients = []
    senddict = dict()
    Lock = threading.Lock()
    debug = True

    def __init__(self, addr: (str, int), delegate):
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind(addr)
            self.server.listen(1)
        except socket.error as e:
            print("[Server.__init__] ERROR binding failed! Msg:", str(e))
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
                        if Server.debug:
                            print("[Server.run.<add>] Client {} connected".format(addr[0]))
                    else:
                        nachricht = sock.recv(1024)
                        ip = sock.getpeername()[0]
                        if nachricht:
                            if Server.debug:
                                print("[Server.run.<recv>] {}: {}".format(ip, nachricht.decode()))
                            self.delegate.handleIncommingMessage(nachricht.decode(), ip)
                        else:
                            sock.close()
                            Server.clients.remove(sock)
                            if sock in schreiben:
                                schreiben.remove(sock)
                            if Server.debug:
                                print("[Server.run.<recv>] Connection with {} closed".format(ip))
                for sock in schreiben:
                    ip = sock.getpeername()[0]
                    if ip in Server.senddict:
                        message = Server.senddict.pop(ip)
                        sock.sendall(bytes(message, 'utf-8'))
                        if Server.debug:
                            print("[Server.run.<send>] {} sent to {} ".format(message, ip))
                if len(Server.senddict) > 0:
                    print("[Server.run.<send>] WARN Not all messages send!")
                Server.Lock.release()
                time.sleep(0.05)
        finally:
            if Server.debug:
                print("[Server.run.<finally>] Closing all clients")
            try:
                for c in Server.clients:
                    c.close()
                self.server.close()
            except socket.error as e:
                print("[Server.run.<finally>] ERROR on closing clients Msg:", str(e))

    def stop(self):
        self._stopme.set()
        if Server.debug:
            print("[Server.stop] stop flag set")

    def stopped(self):
        return self._stopme.isSet()

    def send(self, ip : str, message : str):
        Server.Lock.acquire()
        Server.senddict[ip] = message
        if Server.debug:
            print("[Server.send] Message {} added to senddict".format(message))
        Server.Lock.release()