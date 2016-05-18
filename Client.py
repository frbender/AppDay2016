import socket
import time

class Client():
    def __init__(self, addr : (str,int)):
        self.addr = addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        try:
            self.s.connect(self.addr)
        except socket.error as e:
            print("Error in Client.py: init   " + str(e))

    def send(self, ip = "", message = "") -> bool:
        try:
            self.s.sendall(bytes(message, encoding='utf-8'))
            return True
        except OSError:
            print("Error in Client.py: send")
            return False

    def recv(self) -> str:
        try:
            message = self.s.recv(2048)
            return message.decode()
        except socket.error:
            return ""

    def close(self):
        self.s.close()

c = Client(("127.0.0.1",50000))
c.send(message="Hallo")
time.sleep(1)
c.send(message="noch eine Nachricht")
time.sleep(1)
c.send(message="")
time.sleep(1)
c.send(message="Und Tschüß")
time.sleep(1)
c.close()