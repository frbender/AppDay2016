import threading
from http.server import HTTPServer

import WebTest.AppDayServer as AppDayServer

# Dict, was alle "Actions", also Seiten auf dem Server enthält
# Der Key ist die URL gegeben als regulärer ausdruck
# Tipp: "^\/hallo$" wäre die Url \hallo (also wirklich auch NUR so geschrieben)
# (\/ ist ein ge-escaptes / und ^ bzw. $ markieren anfang/ende vom string)
webActions = {}


# Beispiel für Ableitung unter Benutzung der Template-Klasse
# => SEEEEEEEEEHR EINFACH um ausgaben zu erzeugen
# siehe AppDayServer.py
class HalloSager(AppDayServer.TemplateActionHandler):
    file = "myFile.txt"
    replacements = {"{{Name}}": "Max Mustermann"}


# hinzufügen des Handlers
webActions["^\/hallo$"] = HalloSager()


def run():
    print("Starting Server on Prt 8081...")
    serverAddress = ("127.0.0.1", 8081)
    httpd = HTTPServer(serverAddress, AppDayServer.createWebRequestHandler(webActions))
    print("Running Server...")
    # Threading weil warum nicht? (Blockt ja sonst nach Aufruf von "run()")
    threading.Thread(target=httpd.serve_forever).start()


run()
