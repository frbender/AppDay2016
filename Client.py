import socket


class Client():
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
                print("[Client.__init__] Connected")

    def send(self, ip = "", message = "") -> bool:
        try:
            self.s.sendall(bytes(message, encoding='utf-8'))
            print("[Client.send] Message send")
            return True
        except OSError:
            print("[Client.send] ERROR failed! Msg:", str(e))
            return False

    def recv(self) -> str:
        try:
            message = self.s.recv(2048)
            if not message:
                print("[Client.recv] Closing")
                self.close()
                return None
            else:
                print("[Client.recv] Message receved")
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
            print("[Client.close] Closed!")
        except socket.error as e:
            print("[Client.close] ERROR failed! Msg:", str(e))

# c = Client(("127.0.0.1", 50000))
#
# try:
#
#     while c.isConnectionAlive():
#         nachricht = c.recv()
#         if nachricht:
#             print(nachricht)
#         time.sleep(1)
# finally:
#     print("Closing connection")
#     if c.isConnectionAlive():
#         c.close()