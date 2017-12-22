#!/usr/bin/env python3
# pylint: disable=invalid-name
"""Send images to the e-paper screen"""

from http.server import SimpleHTTPRequestHandler, HTTPStatus
from socketserver import TCPServer
from os import chdir, path
from uuid import uuid4
from binascii import a2b_base64
from PIL import Image
import simplejson


PORT = 3000
SERVER_DIR = path.dirname(path.abspath(__file__))
PUBLIC_DIR = path.realpath(SERVER_DIR + "/../../build")
TMP_DIR = path.realpath(SERVER_DIR + "/../../tmp")


def epd_display_frame(filename_black, filename_red):
    """Print the 2 colors to e-paper"""
    from epd2in13b import EPD
    display = EPD()
    display.init()

    frame_buffer_black = display.get_frame_buffer(Image.open(filename_black))
    frame_buffer_red = display.get_frame_buffer(Image.open(filename_red))
    display.display_frame(frame_buffer_black, frame_buffer_red)

    display.sleep()


class Server(SimpleHTTPRequestHandler):
    """e-paper server"""

    def do_POST(self):
        """Handle POST request"""
        if self.path == "/api/print":
            self.api_print()
        else:
            self.not_found()

    def api_print(self):
        """Print to e-paper display"""
        body = self.rfile.read(int(self.headers['Content-Length']))
        json = simplejson.loads(body)
        # Save image files
        filename = path.join(TMP_DIR, str(uuid4()))
        file_black = open(filename + "_black.png", "wb")
        file_black.write(a2b_base64(json["black"].split(",")[1]))
        file_black.close()
        file_red = open(filename + "_red.png", "wb")
        file_red.write(a2b_base64(json["red"].split(",")[1]))
        file_red.close()
        try:
            epd_display_frame(filename + '_black.png', filename + '_red.png')
        except ImportError:
            print('ImportError (MacOS ?)')

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes("{\"success\": true}", "utf8"))

    def not_found(self):
        """404 response"""
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("404 Page not found", "utf8"))

    def internal_server_error(self):
        """500 response"""
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("500 Internal Server Error", "utf8"))


# httpd = HTTPServer(('', 3000), Webserver)

# httpd.serve_forever()


if __name__ == "__main__":
    print("e-paper-painter running on http://localhost:" + str(PORT) + "/")

    chdir(PUBLIC_DIR)
    TCPServer.allow_reuse_address = True
    TCPServer(('', PORT), Server).serve_forever()
