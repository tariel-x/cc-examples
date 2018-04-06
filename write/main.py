import requests
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

# Register service

f = open('require.json')
query = f.read()

print(query)
r = requests.post(sys.argv[1], data=query)

print(r.content)
print("Register service")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        print(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('0.0.0.0', 8880), SimpleHTTPRequestHandler)
httpd.serve_forever()