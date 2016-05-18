import socket


class Client():
    debug = False

    def __init__(self, addr : (str,int)):
        self.addr = addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        try:
            self.s.connect(self.addr)
        except socket.error as e:
            if e.errno != 36:
                print("[Client.__init__] ERROR connect failed! Msg:", str(e))
            else:
                self.isAlive = True
                if Client.debug:
                    print("[Client.__init__] Connected")

    def send(self, ip = "", message = "") -> bool:
        try:
            self.s.sendall(bytes(message, encoding='utf-8'))
            if Client.debug:
                print("[Client.send] Message send: \"{}\"".format(message))
            return True
        except OSError as e:
            print("[Client.send] ERROR failed! Msg:", str(e))
            return False

    def recv(self) -> str:
        try:
            message = self.s.recv(2048)
            if not message:
                if Client.debug:
                    print("[Client.recv] Closing")
                self.close()
                return None
            else:
                if Client.debug:
                    print("[Client.recv] Message receved: \"{}\"".format(message.decode()))
                return message.decode()
        except socket.error as e:
            #print(str(e))
            return None

    def isConnectionAlive(self) -> bool:
        return self.isAlive

    def close(self):
        self.isAlive = False
        try:
            self.s.close()
            if Client.debug:
                print("[Client.close] Closed!")
        except socket.error as e:
            print("[Client.close] ERROR failed! Msg:", str(e))