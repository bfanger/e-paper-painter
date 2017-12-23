#!/usr/bin/env python
# pylint: disable=invalid-name
"""Send images to the e-paper screen"""

from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer
from os import chdir, path
from uuid import uuid4
from binascii import a2b_base64
import json


PORT = 3000
SERVER_DIR = path.dirname(path.abspath(__file__))
PUBLIC_DIR = path.realpath(SERVER_DIR + "/../../build")
TMP_DIR = path.realpath(SERVER_DIR + "/../../tmp")


def epd_display_frame(filename_black, filename_red):
    """Print the 2 colors to e-paper"""
    from epd2in13b import EPD
    import Image

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
        jsonData = json.loads(body)
        # Save image files
        filename = path.join(TMP_DIR, str(uuid4()))
        file_black = open(filename + "_black.png", "wb")
        file_black.write(a2b_base64(jsonData["black"].split(",")[1]))
        file_black.close()
        file_red = open(filename + "_red.png", "wb")
        file_red.write(a2b_base64(jsonData["red"].split(",")[1]))
        file_red.close()
        try:
            epd_display_frame(filename + '_black.png', filename + '_red.png')
        except ImportError:
            print('ImportError (MacOS ?)')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write("{\"success\": true}")

    def not_found(self):
        """404 response"""
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("404 Page not found")

    def internal_server_error(self):
        """500 response"""
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("500 Internal Server Error")


# httpd = HTTPServer(('', 3000), Webserver)

# httpd.serve_forever()


if __name__ == "__main__":
    print("e-paper-painter running on http://localhost:" + str(PORT) + "/")

    chdir(PUBLIC_DIR)
    TCPServer.allow_reuse_address = True
    TCPServer(('', PORT), Server).serve_forever()
