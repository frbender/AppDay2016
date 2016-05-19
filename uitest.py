import tkinter as Tk
from tkinter import messagebox

class UI_NavMain():
    def Anzeigen(Con: str):
        mlist = Tk.Button(root, text = "ML", command=root.quit, relief = "solid")
        mlist.pack()
        mlist.place(x=0, y=0, width=80, height=60)
        mwrite = Tk.Button(root, text = "MW", command=root.quit, relief = "solid")
        mwrite.pack()
        mwrite.place(x=0, y=60, width=80, height=60)
        settings = Tk.Button(root, text = "SET", command=root.quit, relief = "solid")
        settings.pack()
        settings.place(x=0, y=180, width=80, height=60)
        pexit = Tk.Button(root, text = "QUIT", command=root.quit, relief = "solid")
        pexit.pack()
        pexit.place(x=240, y=180, width=80, height=60)

        topborder = Tk.Canvas()
        topborder.pack()
        topborder.place(x=80, y=-2, width=243, height=25)
        topborder.create_line(0, 3, 243, 3, width=1)  # Linie Oben
        topborder.create_line(0, 23, 243, 23, width=1)  # Linie Unten
        topborder.create_line(1, 3, 1, 25, width=1)  # Linie Links
        topborder.create_line(213, 3, 213, 25, width=1)  # Linie zwischen Countdown/Connection
        topborder.create_text(225, 13, text=Con)

class UI_NavMenu():
    def Anzeigen(root, AktSeite : int, GesSeite : int , InfoText : str, Con : str):
        back = Tk.Button(root, text = "<", command=root.quit, relief = "solid")
        back.pack()
        back.place(x=0, y=0, width=80, height=60)

        up = Tk.Button(root, text = "u", command=root.quit, relief = "solid")
        up.pack()
        up.place(x=0, y=60, width=80, height=90)

        down = Tk.Button(root, text = "D", command=root.quit, relief = "solid")
        down.pack()
        down.place(x=0, y=150, width=80, height=90)

        topborder = Tk.Canvas()
        topborder.pack()
        topborder.place(x=80, y=-2, width=243, height=25)
        topborder.create_line(0, 3, 243, 3, width=1)        #Linie Oben
        topborder.create_line(0, 23, 243, 23, width=1)      #Linie Unten
        topborder.create_line(1, 3, 1, 25, width=1)         #Linie Links
        topborder.create_line(60, 3, 60, 25, width=1)       #Linie zwischen Page/Countdown
        topborder.create_line(213, 3, 213, 25, width=1)     #Linie zwischen Countdown/Connection
        #topborder.create_line(237, 0, 237, 30, width=1)
        topborder.create_text(15, 13, text= str(AktSeite) + "/" + str(GesSeite), width=100, justify="right")
        topborder.create_text(100, 13, text=InfoText)
        topborder.create_text(225, 13, text=Con)

class UI_MainInfos():
    def Anzeigen(Anzahl : int, InfoText : str):
        messages = Tk.Label(root, text = str(Anzahl) + " ungelesene Nachrichten\n\n" + InfoText, wraplength = 240)
        messages.pack()
        messages.place(x=80, y=28, width=240, height=115)

class UI_NachrichtenListe():
    def Anzeigen(Anzahl : int, From1 : str, Text1 : 1, From2 : str, Text2 : str, From3 : str, Text3 : str):
        elements = ["element1", "element2", "element3"]
        for i in range(Anzahl):
            elements[i] = Tk.Button(root)
            if i == 0: elements[i]["text"] = From1 + ":" + Text1
            if i == 1: elements[i]["text"] = From2 + ":" + Text2
            if i == 2: elements[i]["text"] = From3 + ":" + Text3
            elements[i]["relief"] = "solid"
            elements[i].pack()
            elements[i].place(x=80, y=28 + (i * 71), width=240, height=71)

class UI_NachrichtLesen():
    def Anzeigen(From : str, Message : str):
        nachricht = Tk.Label(root, text=From + " schrieb:\n\n" + Message, justify = "left", anchor = "nw", wraplength=240)
        nachricht.pack()
        nachricht.place(x=80, y=28, width=240, height=215)

class UI_NachrichtSchreiben():
    def Anzeigen(Anzahl : int, Label1 : str, Label2 : str, Label3 : str, InfoText : str):
        elements = ["element1", "element2", "element3"]
        for i in range(Anzahl):
            elements[i] = Tk.Button(root)
            if i == 0: elements[i]["text"] = Label1
            if i == 1: elements[i]["text"] = Label2
            if i == 2: elements[i]["text"] = Label3
            elements[i]["relief"] = "solid"
            elements[i].pack()
            elements[i].place(x=105 + (i * 65), y=50, width=60, height=60)

        bottomborder = Tk.Canvas()
        bottomborder.pack()
        bottomborder.place(x=80, y=180, width=180, height=60)
        bottomborder.create_line(0, 3, 243, 3, width=1)  # Linie Oben
        bottomborder.create_line(0, 53, 243, 53, width=1)  # Linie Unten

        psend = Tk.Button(root, text="SEND", relief="solid")
        psend.pack()
        psend.place(x=260, y=180, width=60, height=60)

# root = Tk.Tk()
#
# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
# root.overrideredirect(1)
# root.geometry("%dx%d+0+0" % (w, h))
#
#
# #UI_NachrichtSchreiben.Anzeigen(3, "Ja", "Nein", "Egal", "Ja!!!!")
# #UI_MainInfos.Anzeigen(3, "23:12:55")
# #UI_NachrichtenListe.Anzeigen(3, "Master", "Hallo Welt1", "Slave1", "Eintrag 2", "Slave2", "Eintrag3")
# #UI_NachrichtLesen.Anzeigen("Master", "Hallo Team! Ich hoffe ihr kommt mit eurem Projekt voran und wir sehen uns gleich.")
#
# UI_NavMain.Anzeigen("ok")
#
# root.mainloop()