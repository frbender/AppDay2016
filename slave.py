import tkinter as Tk

from Communication.CommunicationManager import ClientCommunicationManager
from Communication.ProtocolHandler import ProtocolMessage
from UI.led import LedHandler

NICKNAME = "PETER"
ADDR = ("192.168.0.101", 50000)


class MainClass:
    statements = {1: "Jo", 2: "Ne", 3: "Ziiiimmerseeervice, bitte!",
                  4: "Assistence Required!"}
    msgPointer = 0
    readTo = 0

    def __init__(self):
        self.cmgr = ClientCommunicationManager(self, ADDR, NICKNAME)
        self.messages = [ProtocolMessage("GOTT", "", "MESSAGE", "Keine weiteren Nachrichten")]
        self.root = Tk.Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.cmgr.subscribe()
        self.showNachricht("")
        self.lh = LedHandler(True)

    def showNachricht(self, msgtext):
        self.left = Tk.Button(command=(lambda: self.back()), text="<=")
        self.left.pack()
        self.left.place(x=0, y=0, width=48, height=96)

        font = ("Arial", 10, "normal")

        self.nachricht = Tk.Label(text=msgtext, font=font, wraplength=200)
        self.nachricht.pack()
        self.nachricht.place(x=48, y=0, width=320 - 48 - 48, height=96)

        self.right = Tk.Button(command=(lambda: self.forth()), text="=>")
        self.right.pack()
        self.right.place(x=320 - 48, y=0, width=48, height=96)

        self.one = Tk.Button(command=(lambda: self.btnClick(1)), text=self.statements[1], wraplength=100)
        self.one.pack()
        self.one.place(x=0, y=96, width=160, height=(240 - 96) / 2 - 16)

        self.two = Tk.Button(command=(lambda: self.btnClick(2)), text=self.statements[2], wraplength=100)
        self.two.pack()
        self.two.place(x=160, y=96, width=160, height=(240 - 96) / 2 - 16)

        self.three = Tk.Button(command=(lambda: self.btnClick(3)), text=self.statements[3], wraplength=100)
        self.three.pack()
        self.three.place(x=0, y=96 + (240 - 96) / 2 - 16, width=160, height=(240 - 96) / 2 - 16)

        self.four = Tk.Button(command=(lambda: self.btnClick(4)), text=self.statements[4], wraplength=100)
        self.four.pack()
        self.four.place(x=160, y=96 + (240 - 96) / 2 - 16, width=160, height=(240 - 96) / 2 - 16)

        self.textfield = Tk.Entry(bd=1)
        self.textfield.pack()
        self.textfield.place(x=0, y=240 - 32, width=320, height=32)
        self.textfield.focus_set()

        self.root.bind("<Return>", lambda x: self.sendCustom())

        self.updateLabel()

        self.root.mainloop()

    def sendCustom(self):
        x = self.textfield.get()
        print(x)
        self.cmgr.sendMessage(x)
        self.textfield.delete(0, len(x))

    def btnClick(self, btnNumber):
        print(self.statements[btnNumber])
        self.cmgr.sendMessage(self.statements[btnNumber])
        return

    def back(self):
        if self.msgPointer > 0:
            self.msgPointer -= 1
            self.updateLabel()

    def forth(self):
        if self.msgPointer < len(self.messages) - 1:
            self.msgPointer += 1
            if self.msgPointer < self.readTo:
                self.readTo = self.msgPointer
        if self.msgPointer == len(self.messages) - 1:
            self.lh.on = False
        self.updateLabel()

    def updateLabel(self):
        self.nachricht["text"] = "[{} {}/{}]: ".format(self.messages[self.msgPointer].m_from, self.msgPointer + 1,
                                                       len(self.messages)) + self.messages[
                                     self.msgPointer].m_content

    def addNewMessage(self, msg: ProtocolMessage):
        self.messages.append(msg)
        self.updateLabel()
        self.lh = LedHandler(True)
        self.lh.start()


print("START")
main = MainClass()
print("ENDE")
