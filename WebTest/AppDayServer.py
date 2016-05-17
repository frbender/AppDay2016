import re
from http.server import BaseHTTPRequestHandler


# Beispielklasse für einen Handler, der eine Ausgabe liefert
# (ist auch die minimale bauweise)
class ActionHandler():
    def handle(self, relativeurl: str, postdata: dict, headers: dict) -> str:
        print("Default handler called :) (\"" + relativeurl + "\")")
        return "Default handler :)"


# Beispielklasse, wie man mit "Templates arbeiten könnte"
# file = datei
# replacements = dict, wobei key = zu ersetzender text und value = neuer text
class TemplateActionHandler(ActionHandler):
    file = ""
    replacements = {}

    def handle(self, relativeurl: str, postdata: dict, headers: dict):
        f = open(self.file, 'r')
        o = f.read()
        for replacement in self.replacements:
            o = o.replace(replacement, self.replacements[replacement])
        return o


# Muss eigentlich garnicht angefasst werden
class WebRequestHandler(BaseHTTPRequestHandler):
    actions = {}
    defaultAction = ActionHandler()

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
    return type('WebHandler', (WebRequestHandler,), {'actions': actions})
