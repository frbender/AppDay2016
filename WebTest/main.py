from http.server import BaseHTTPRequestHandler, HTTPServer


class WebRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


a = [1, 2, 3, 4, 5]

def reverse(x):
    if len(x) == 0:
        return []
    a, b = (x[0], x[1:])
    return reverse(b) + [a]

print(reverse(a))


def run():
    print("starting server...")
    serverAddress = ("127.0.0.1", 8081)
    httpd = HTTPServer(serverAddress, WebRequestHandler)
    print("running server...")
    httpd.serve_forever()


run()
