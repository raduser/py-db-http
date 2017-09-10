from http.server import BaseHTTPRequestHandler, HTTPServer
import dbhandler

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("got".encode("utf-8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        dbarray = [[], []]
        self._set_headers()
        content = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content)
        dbhandler.on_parse(post_body, dbarray, self)
        self.wfile.write("posted".encode("utf-8"))

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()