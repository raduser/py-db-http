from http.server import BaseHTTPRequestHandler, HTTPServer
import dbhandler


class Handler(BaseHTTPRequestHandler):
    DBArray = []

    def _make_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _make_headers_error(self, response):
        try:
            self.send_error(400, response [0].encode("utf-8"), response[1:len(response)].encode("utf-8"))
        except IndexError:
            self.send_error(400, response[0])

    def response_handler(self, response):
        if response[0]:
            if response[0] == "Error":
                self._make_headers_error(response)
            else:
                self._make_headers()
                self.DBArray = response
                response_processed = ""
                for i in range(len(response)):
                    response_processed += str(i) + ' ' + str(self.DBArray[int(i)]) + "\n"
                    print(response_processed)
                self.wfile.write(response_processed.encode("utf-8"))
        else:
            self._make_headers_error(dbhandler.simple_parse("Unknown error"))

    def do_POST(self):
        post_body = self.headers.get_all('Content-Length', 0)
        post_body = self.rfile.read(int(post_body[0]))
        response = dbhandler.on_parse(post_body, self.DBArray, self)
        print(response)
        self.response_handler(response)


def run(server_class=HTTPServer):
    server_address = ('', 7000) #goes for localhost:7000
    httpd = server_class(server_address, Handler)
    httpd.serve_forever()

run()
