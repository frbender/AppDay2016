import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

webActions = {}


class ActionHandler():
    def handle(self, relativeUrl: str, postData: dict, headers: dict) -> str:
        print("Default handler called :) (\"" + relativeUrl + "\")")
        return "Default handler :)"


class TemplateActionHandler(ActionHandler):
    file = ""
    replacements = {}

    def handle(self, relativeUrl: str, postData: dict, headers: dict):
        f = open(self.file, 'r')
        o = f.read()
        for replacement in self.replacements:
            o = o.replace(replacement, self.replacements[replacement])
        return o


class HalloSager(TemplateActionHandler):
    file = "myFile.txt"
    replacements = {"{{Name}}": "Max Mustermann"}


webActions["^\/hallo$"] = HalloSager()

class WebRequestHandler(BaseHTTPRequestHandler):
    actions = {}
    defaultAction = ActionHandler()

    # Fügt eine neue Action dem Webserver hinzu
    # Beispiel (...).addAction("\/[a-zA-Z]+\/.*", myAction)
    def addAction(self, url: str, action: ActionHandler):
        if url in self.actions.keys():
            print(url + " allready in actions!")
        else:
            self.actions[url] = action

    # Wird bei einem GET aufgerufen
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ""
        successful = False

        for action in self.actions:
            if re.match(action, self.path):
                output = self.actions[action].handle(self.path, {}, self.headers)
                successful = True
                break

        if not successful:
            output = self.defaultAction.handle(self.path, {}, self.headers)

        self.wfile.write(bytes(output, "utf8"))
        return


# Erzeugt einen neuen Type "WebHandler", der die actions enthält
# (wird von HTTPServer gebraucht)
def createWebRequestHandler(actions):
    return type('WebHandler', (WebRequestHandler,), {'actions': webActions})

def run():
    print("Starting Server on Prt 8081...")
    serverAddress = ("127.0.0.1", 8081)
    httpd = HTTPServer(serverAddress, createWebRequestHandler(webActions))
    print("Running Server...")
    threading.Thread(target=httpd.serve_forever).start()

run()
print("Yo")
