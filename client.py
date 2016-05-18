import socket


class Client():
    def __init__(self, ip : str):
        self.ip = ip
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        try:
            self.s.connect((ip, 50000))
        except socket.error:
            print("Error in client.py: init")

    def send(self, ip : str, message : str) -> bool:
        try:
            self.s.sendall(message)
            return True
        except OSError:
            print("Error in client.py: send")
            return False

    def recv(self) -> str:
        try:
            message = self.s.recv(2048)
            return message.decode()
        except socket.error:
            return ""
