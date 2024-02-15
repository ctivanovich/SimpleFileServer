import argparse
import http.server
import os
import socketserver

PORT = 8000

class HttpFileRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()

        self.wfile.write(bytes(str(os.listdir()), "utf8"))
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.send_response(200)

if __name__ == "__main__":

    handler = HttpFileRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("Server started at localhost:" + str(PORT))
        httpd.serve_forever()