from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import sys
import subprocess
import html

def is_xdotool_installed():
    try:
        subprocess.run(["xdotool", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

def emulate_key_press(key):
    try:
        subprocess.run(["xdotool", "key", key])
    except Exception as e:
        print(f"Error: {e}")

class  lebraRequestHandler(BaseHTTPRequestHandler):
           
    def do_GET(self):
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = urllib.parse.parse_qs(post_data)
        
        if 'barcode' in parsed_data:
            barcode = parsed_data['barcode'][0]
            barcodeHTML = html.escape(barcode)
            print(f"Scanned: {barcode}")
            
            for char in barcode:
                emulate_key_press(char)

            message = f'<div style="background-color:#060; color: white;">Success - Scanned {barcodeHTML}</div>'
        else:
            message = '<div style="background-color:#600; color: white;">ERROR</div>'
            
        html_content = self.get_HTML(message)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
        
    def get_HTML(self, message=""):
        html_content = """
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
                    <div id="message">{}</div>
                </body>
            </html>
            """.format(message)
        return html_content

if __name__ == '__main__':
    port = 8998
    server_address = ('', port)
    
    if not is_xdotool_installed():
        print("Can not find xdotool. Please install or check PATH")
        sys.exit(1)

    with HTTPServer(server_address,  lebraRequestHandler) as httpd:
        print(f'Starting server on port {port}...')
        httpd.serve_forever()
