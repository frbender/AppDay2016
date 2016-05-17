import re
from http.server import BaseHTTPRequestHandler

# Beispielklasse für einen Handler, der eine Ausgabe liefert
# (ist auch die minimale bauweise)
class ActionHandler():
    def getheaders(self, handler):
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()

    def handle(self, relativeurl: str, postdata: dict, headers: dict) -> str:
        print("Default handler called :) (\"" + relativeurl + "\")")
        return "Default handler :)"

    def needsencoding(self):
        return True


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


# Beispielklasse, wie man mit "Templates arbeiten könnte"
# file = datei
# replacements = dict, wobei key = zu ersetzender text und value = neuer text
class BinaryActionHandler(ActionHandler):
    def getheaders(self, handler):
        handler.send_response(200)
        if ".jpg" in handler.path:
            handler.send_header('Content-type', 'image/jpeg')
        elif ".png" in handler.path:
            handler.send_header('Content-type', 'image/png')
        else:
            handler.send_header('Content-type', 'application / force - download')
        handler.end_headers()

    def handle(self, relativeurl: str, postdata: dict, headers: dict):
        f = open("." + relativeurl, 'rb')
        return f.read()  # What could possibly go wrong?

    def needsencoding(self):
        return False


# Muss eigentlich garnicht angefasst werden
class WebRequestHandler(BaseHTTPRequestHandler):
    actions = {}
    defaultAction = ActionHandler()

    # Wird bei einem GET aufgerufen
    def do_GET(self):

        output = ""
        successful = False

        for action in self.actions:
            if re.match(action, self.path):
                self.actions[action].getheaders(self)
                output = self.actions[action]
                successful = True
                break

        if not successful:
            self.defaultAction.getheaders(self)
            output = self.defaultAction
        if output.needsencoding():
            output = bytes(output.handle(self.path, {}, self.headers), "utf8")
        else:
            output = output.handle(self.path, {}, self.headers)
        self.wfile.write(output)
        return


# Erzeugt einen neuen Type "WebHandler", der die actions enthält
# (wird von HTTPServer gebraucht)
def createWebRequestHandler(actions):
    return type('WebHandler', (WebRequestHandler,), {'actions': actions})
