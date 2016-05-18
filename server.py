import socket
import threading
import socketserver


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        addr = self.client_address[0]
        print("[{}] Verbindung hergestellt".format(addr))

        while True:
            s = self.request.recv
            if s:
                # Hier sind die Daten gesendeten Daten verfügbar
                print("[{}] {}".format(addr, s.decode()))
            else:
                print("[{}] Verbindung geschlossen".format(addr))
                break


class Server:
    def __init__(self, addr : (str,int)):
        try:
            self.server = server = ThreadedTCPServer(addr, ThreadedTCPRequestHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.deamon = True
            self.server_thread.start()
            print("Server loop running in thread:", self.server_thread.name)
        except socket.error:
            print("Error in server.py: Server.__init__")

    def shutdown_server(self):
        self.server.shutdown()

    def send(self):
        pass

    def recv(self):
        pass
