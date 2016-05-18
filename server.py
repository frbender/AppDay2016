import signal
import socketserver
import sys


class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        addr = self.client_address[0]
        print("[{}] Verbindung hergestellt".format(addr))

        while True:
            s = self.request.recv(1024)
            if s:
                # Hier sind die Daten gesendeten Daten verfügbar
                print("[{}] {}".format(addr, s.decode()))
            else:
                print("[{}] Verbindung geschlossen".format(addr))
                break

def signalHandler(signal, frame):
    global server
    print("Closing because of kill")
    server.shutdown()
    sys.exit(0)


signal.signal(signal.SIGTERM, signalHandler)
server = socketserver.ThreadingTCPServer(("", 50000), ChatRequestHandler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.shutdown()
