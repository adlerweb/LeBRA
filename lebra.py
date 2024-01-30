#!/usr/bin/env python3

"""LeBRA - Legacy Barcode Reader Application"""

import html
import argparse
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pynput.keyboard import Key, Controller

def emulate_key_presses(text):
    """Send supplied text as key presses"""
    try:
        keyboard.type(text)
        if args.enter:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
    except Exception as error:
        print(f"Error: {error}")

class LebraRequestHandler(BaseHTTPRequestHandler):
    """HTTP handlers"""
    def do_GET(self):
        """Handle GET requests and show form"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # HTML form with action and method attributes
            html_content = self.get_HTML()

            self.wfile.write(html_content.encode('utf-8'))

        elif self.path == '/submit':
            self.do_POST()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Handle POST requests and process barcodes"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)

        if 'barcode' in parsed_data:
            barcode = parsed_data['barcode'][0]
            barcode_html = html.escape(barcode)
            curdt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Scanned: {barcode} at {curdt}")

            emulate_key_presses(barcode)

            message = '<div style="background-color:#060; color: white;">'
            message = message + f'Success - Scanned {barcode_html} at {curdt}</div>'
        else:
            message = '<div style="background-color:#600; color: white;">ERROR</div>'

        html_content = self.get_HTML(message)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def get_HTML(self, message=""):
        """Generate HTML form"""
        html_content = f"""
            <html>
                <head>
                    <title>LeBRA - Legacy Bardocde Reader Application</title>
                    <style>font-size: 300%;</style>
                </head>
                <body onload="var input = document.getElementById('barcode').focus();">
                    <h1>LeBRA - Legacy Bardocde Reader Application</h1>
                    <form action="/submit" method="post">
                        <label for="barcode">Barcode:</label>
                        <input type="text" id="barcode" name="barcode" autofocus>
                        <br>
                        <input type="submit" value="Submit">
                    </form>
                    <div id="message">{message}</div>
                </body>
            </html>
            """
        return html_content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Emulate keyboard input')
    parser.add_argument('-e', '--enter', action='store_true',
        help='Press and release the Enter key after typing')
    parser.add_argument('-l', '--listen', default='', metavar="IP-ADDRESS",
        help='Specify the listen address. Listen on all addresses if not specified.')

    parser.add_argument('-p', '--port', type=int, default=8998,
        help='Specify the port number for HTTP server (default: 8998)')


    args = parser.parse_args()

    server_address = (args.listen, args.port)

    keyboard = Controller()

    with HTTPServer(server_address, LebraRequestHandler) as httpd:
        print(f'Starting server on {args.listen}:{args.port}...')
        httpd.serve_forever()
